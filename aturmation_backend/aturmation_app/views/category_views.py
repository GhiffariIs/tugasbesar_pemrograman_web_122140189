from pyramid.view import view_config
from pyramid.response import Response # Tidak terpakai jika semua pakai HTTPExceptions
from pyramid.httpexceptions import (
    HTTPCreated,
    HTTPOk,
    HTTPNotFound,
    HTTPBadRequest,
    HTTPNoContent,
    HTTPForbidden # Untuk kasus permission denied jika tidak ditangani ACL secara otomatis
)
from sqlalchemy.exc import IntegrityError, DBAPIError

from ..models.category import Category
from ..models.user import User, UserRole
# Impor UserRole jika Anda ingin menggunakan role dalam logika view,
# tapi biasanya permission cukup di @view_config dan ACL
# from ..models.user import UserRole 

# --- Definisikan Nama Permission (string) ---
# Sebaiknya konsisten dengan yang akan Anda definisikan di security.py (RootACL)
VIEW_CATEGORY_PERMISSION = 'category:view'
ADD_CATEGORY_PERMISSION = 'category:add'
EDIT_CATEGORY_PERMISSION = 'category:edit'
DELETE_CATEGORY_PERMISSION = 'category:delete'

@view_config(
    route_name='api_categories_collection',
    request_method='POST',
    renderer='json',
    permission=ADD_CATEGORY_PERMISSION # Permission untuk membuat kategori
)
def create_category_view(request):
    try:
        data = request.json_body
        name = data.get('name')
        description = data.get('description') # Deskripsi opsional

        if not name:
            raise HTTPBadRequest(json_body={'message': 'Category name is required.'})
        if len(name) > 100: # Contoh validasi panjang
             raise HTTPBadRequest(json_body={'message': 'Category name cannot exceed 100 characters.'})


        print(f"[DEBUG] create_category_view: Attempting to create category '{name}'")

        new_category = Category(name=name, description=description)
        request.dbsession.add(new_category)
        # Flush untuk mendapatkan ID dan error DB lebih awal (seperti unique constraint)
        # pyramid_tm akan menangani commit/rollback di akhir request yang sukses/gagal.
        request.dbsession.flush() 
        
        print(f"[DEBUG] create_category_view: Category '{name}' flushed with ID {new_category.id}")
        
        return HTTPCreated(json_body={
            'message': 'Category created successfully.',
            'category': new_category.as_dict()
        })
    except IntegrityError: # Jika nama kategori duplikat (karena unique=True di model)
        request.dbsession.rollback()
        print(f"[DEBUG] create_category_view: IntegrityError for name '{name}'")
        return HTTPBadRequest(json_body={'message': f"Category with name '{name}' already exists."})
    except DBAPIError as e:
        request.dbsession.rollback()
        print(f"[DEBUG] create_category_view: DBAPIError - {e}")
        return Response("Database error during category creation.", status=500) # Respons generik 500
    except ValueError: # Jika request.json_body gagal parse
        print("[DEBUG] create_category_view: ValueError (bad JSON)")
        return HTTPBadRequest(json_body={'message': 'Invalid JSON format in request body.'})
    except Exception as e: # Tangkap error tak terduga lainnya
        request.dbsession.rollback()
        print(f"[DEBUG] create_category_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)


@view_config(
    route_name='api_categories_collection',
    request_method='GET',
    renderer='json',
    permission=VIEW_CATEGORY_PERMISSION # Permission untuk melihat semua kategori
)
def get_all_categories_view(request):
    try:
        print("[DEBUG] get_all_categories_view: Fetching all categories")
        # TODO: Pertimbangkan pagination jika data kategori sangat banyak di masa depan.
        # Untuk sekarang, kita ambil semua.
        # page = int(request.params.get('page', 1))
        # limit = int(request.params.get('limit', 10))
        # offset = (page - 1) * limit
        # categories_query = request.dbsession.query(Category).order_by(Category.name)
        # total_categories = categories_query.count()
        # categories = categories_query.offset(offset).limit(limit).all()
        
        categories = request.dbsession.query(Category).order_by(Category.name).all()
        return {'categories': [category.as_dict() for category in categories]}
    except DBAPIError as e:
        print(f"[DEBUG] get_all_categories_view: DBAPIError - {e}")
        return Response("Database error fetching categories.", status=500)
    except Exception as e:
        print(f"[DEBUG] get_all_categories_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)


@view_config(
    route_name='api_category_detail',
    request_method='GET',
    renderer='json',
    permission=VIEW_CATEGORY_PERMISSION # Permission untuk melihat satu kategori
)
def get_category_view(request):
    try:
        category_id = request.matchdict.get('id')
        print(f"[DEBUG] get_category_view: Fetching category with ID {category_id}")
        
        category = request.dbsession.query(Category).get(category_id)
        
        if not category:
            print(f"[DEBUG] get_category_view: Category ID {category_id} not found")
            raise HTTPNotFound(json_body={'message': 'Category not found.'})
        
        return {'category': category.as_dict()}
    except DBAPIError as e: # Menangkap error jika category_id bukan integer, dll.
        print(f"[DEBUG] get_category_view: DBAPIError (likely invalid ID format or DB issue) - {e}")
        # Jika ID tidak valid (bukan integer), query .get() mungkin gagal atau return None.
        # Jika ID valid tapi tidak ada, HTTPNotFound di atas yang akan terpicu.
        return HTTPBadRequest(json_body={'message': 'Invalid category ID format or database error.'})
    except Exception as e:
        print(f"[DEBUG] get_category_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)


@view_config(
    route_name='api_category_detail',
    request_method='PUT',
    renderer='json',
    permission=EDIT_CATEGORY_PERMISSION # Permission untuk update kategori
)
def update_category_view(request):
    try:
        category_id = request.matchdict.get('id')
        print(f"[DEBUG] update_category_view: Attempting to update category ID {category_id}")

        category = request.dbsession.query(Category).get(category_id)
        if not category:
            print(f"[DEBUG] update_category_view: Category ID {category_id} not found for update")
            raise HTTPNotFound(json_body={'message': 'Category not found.'})

        data = request.json_body
        updated_fields = []

        if 'name' in data:
            new_name = data['name']
            if not new_name: # Nama tidak boleh kosong
                 raise HTTPBadRequest(json_body={'message': 'Category name cannot be empty.'})
            if len(new_name) > 100:
                 raise HTTPBadRequest(json_body={'message': 'Category name cannot exceed 100 characters.'})
            
            # Cek duplikasi nama jika nama diubah dan tidak sama dengan nama lama
            if category.name != new_name:
                existing_category_with_new_name = request.dbsession.query(Category).filter(
                    Category.name == new_name, 
                    Category.id != category_id # Pastikan bukan kategori yang sama
                ).first()
                if existing_category_with_new_name:
                    print(f"[DEBUG] update_category_view: IntegrityError - name '{new_name}' already exists.")
                    raise HTTPBadRequest(json_body={'message': f"Category with name '{new_name}' already exists."})
            category.name = new_name
            updated_fields.append('name')
        
        if 'description' in data: # description boleh null/kosong
            category.description = data.get('description') # .get() aman jika field tidak ada
            updated_fields.append('description')
        
        if not updated_fields:
            # Jika tidak ada field yang diupdate, bisa kembalikan data asli atau pesan.
            # Frontend mungkin mengharapkan data terupdate meskipun tidak ada perubahan.
            return HTTPOk(json_body={
                'message': 'No changes detected for category.',
                'category': category.as_dict()
            })

        # request.dbsession.add(category) # Tidak perlu .add() untuk objek yang sudah di-track sesi
        request.dbsession.flush() # Untuk menjalankan validasi dan mendapatkan error DB lebih awal
        print(f"[DEBUG] update_category_view: Category ID {category_id} updated. Fields: {updated_fields}")
        
        return HTTPOk(json_body={
            'message': 'Category updated successfully.',
            'category': category.as_dict()
        })
    except IntegrityError: # Seharusnya sudah ditangani oleh cek duplikasi eksplisit di atas
        request.dbsession.rollback()
        print(f"[DEBUG] update_category_view: IntegrityError during flush (unexpected).")
        return HTTPBadRequest(json_body={'message': f"Category name conflict during update."})
    except DBAPIError as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_category_view: DBAPIError - {e}")
        return Response("Database error updating category.", status=500)
    except ValueError: # Jika request.json_body gagal parse
        print(f"[DEBUG] update_category_view: ValueError (bad JSON)")
        return HTTPBadRequest(json_body={'message': 'Invalid JSON format in request body.'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] update_category_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)


@view_config(
    route_name='api_category_detail',
    request_method='DELETE',
    renderer='json', # renderer='json' akan membuat HTTPNoContent mengembalikan body JSON kosong jika ada, atau tidak sama sekali.
                    # Jika ingin benar-benar tanpa body, renderer tidak perlu diset atau gunakan renderer khusus.
                    # Tapi HTTPNoContent() dari pyramid.httpexceptions sudah benar.
    permission=DELETE_CATEGORY_PERMISSION # Permission untuk hapus kategori
)
def delete_category_view(request):
    try:
        category_id = request.matchdict.get('id')
        print(f"[DEBUG] delete_category_view: Attempting to delete category ID {category_id}")

        category = request.dbsession.query(Category).get(category_id)
        if not category:
            print(f"[DEBUG] delete_category_view: Category ID {category_id} not found for deletion")
            raise HTTPNotFound(json_body={'message': 'Category not found.'})

        # PERHATIAN: Logika untuk mengecek apakah kategori ini digunakan oleh Produk
        # perlu ditambahkan di sini sebelum menghapus. Jika digunakan, Anda mungkin ingin:
        # 1. Mencegah penghapusan dan mengembalikan error (misal, HTTPConflict 409).
        # 2. Meng-set category_id di produk terkait menjadi NULL (jika diizinkan).
        # 3. Menghapus produk terkait juga (cascade delete, hati-hati!).
        # Untuk sekarang, kita hapus langsung.
        # Contoh cek (membutuhkan model Product):
        # from ..models.product import Product # Perlu impor Product
        # if request.dbsession.query(Product).filter_by(categoryId=category_id).first():
        #     raise HTTPBadRequest(json_body={'message': 'Cannot delete category: It is currently in use by one or more products.'})

        request.dbsession.delete(category)
        # pyramid_tm akan menangani commit/rollback. flush() opsional di sini.
        # request.dbsession.flush() 
        print(f"[DEBUG] delete_category_view: Category ID {category_id} deleted from session.")
        
        return HTTPNoContent() # Status 204, secara default tidak ada body.
                               # Frontend Anda mengharapkan pesan sukses, jadi ini mungkin perlu disesuaikan
                               # atau frontend menangani 204 sebagai sukses.
                               # Jika frontend butuh body: return HTTPOk(json_body={'message': 'Category deleted'})
                               # tapi 204 lebih standar untuk DELETE sukses tanpa konten.

    except DBAPIError as e: 
        request.dbsession.rollback()
        # Jika ada foreign key constraint dari tabel Product yang mencegah penghapusan
        print(f"[DEBUG] delete_category_view: DBAPIError (likely FK violation) - {e}")
        return HTTPBadRequest(json_body={'message': 'Error deleting category. It might be in use or a database error occurred.'})
    except Exception as e:
        request.dbsession.rollback()
        print(f"[DEBUG] delete_category_view: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return Response(f"An unexpected error occurred: {e}", status=500)