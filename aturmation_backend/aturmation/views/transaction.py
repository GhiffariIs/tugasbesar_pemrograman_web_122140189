from pyramid.view import view_defaults, view_config
from ..models.transaction import Transaction, TransactionType
from ..models.product import Product
from .base import BaseView
from pyramid.httpexceptions import HTTPNotFound
import json
from sqlalchemy import desc


@view_defaults(route_name='transactions', renderer='json')
class TransactionView(BaseView):
    
    @view_config(request_method='GET', permission='user')
    def get_all_transactions(self):
        try:
            transactions = self.dbsession.query(Transaction).order_by(
                desc(Transaction.tanggal_transaksi)
            ).all()
            return self.json_response([trans.to_dict() for trans in transactions])
        except Exception as e:
            return self.error_response(str(e), 500)
            
    @view_config(request_method='POST', permission='user')
    def create_transaction(self):
        try:
            body = self.request.json_body
            produk_id = body.get('produk_id')
            jumlah = body.get('jumlah')
            jenis_transaksi = body.get('jenis_transaksi')
            
            if not produk_id or not jumlah or not jenis_transaksi:
                return self.error_response(
                    "produk_id, jumlah, and jenis_transaksi are required fields", 
                    400
                )
            
            # Validate transaction type
            if jenis_transaksi not in ['masuk', 'keluar']:
                return self.error_response(
                    "jenis_transaksi must be either 'masuk' or 'keluar'", 
                    400
                )
                
            # Check if product exists
            product = self.dbsession.query(Product).filter_by(id=produk_id).first()
            if not product:
                return self.error_response("Product not found", 400)
                
            # For outgoing transactions, check stock level
            if jenis_transaksi == 'keluar' and jumlah > product.stok:
                return self.error_response(
                    f"Not enough stock. Current stock: {product.stok}", 
                    400
                )
            
            # Create transaction
            transaction = Transaction(
                produk_id=produk_id,
                jumlah=jumlah,
                jenis_transaksi=TransactionType[jenis_transaksi]
            )
            
            # Update product stock
            if jenis_transaksi == 'masuk':
                product.stok += jumlah
            else:  # keluar
                product.stok -= jumlah
                
            self.dbsession.add(transaction)
            self.dbsession.flush()
            
            return self.json_response({
                **transaction.to_dict(),
                'current_stock': product.stok
            }, status=201)
        except Exception as e:
            return self.error_response(str(e), 500)


@view_defaults(route_name='transaction_item', renderer='json')
class TransactionItemView(BaseView):
    
    @view_config(request_method='GET', permission='user')
    def get_transaction(self):
        try:
            transaction_id = int(self.request.matchdict['id'])
            transaction = self.dbsession.query(Transaction).filter_by(id=transaction_id).first()
            
            if not transaction:
                return self.error_response("Transaction not found", 404)
                
            return self.json_response(transaction.to_dict())
        except Exception as e:
            return self.error_response(str(e), 500)
