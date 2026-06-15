const API_URL = 'http://127.0.0.1:8000/api/products';

const modal = document.getElementById('productModal');
const addBtn = document.getElementById('addBtn');
const closeBtn = document.querySelector('.close-btn');
const productForm = document.getElementById('productForm');
const tableBody = document.getElementById('tableBody');
const modalTitle = document.getElementById('modalTitle');

// Modal aç/kapat
addBtn.onclick = () => {
    productForm.reset();
    document.getElementById('productId').value = '';
    modalTitle.textContent = 'Yeni Ürün Ekle';
    modal.style.display = 'flex';
}

closeBtn.onclick = () => { modal.style.display = 'none'; }
window.onclick = (event) => {
    if (event.target == modal) modal.style.display = 'none';
}

// Ürünleri Getir
async function fetchProducts() {
    try {
        const response = await fetch(`${API_URL}/`);
        const products = await response.json();
        renderTable(products);
    } catch (error) {
        console.error('Hata:', error);
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--danger-color);">API bağlantı hatası! MSSQL sunucusunun çalıştığından emin olun.</td></tr>`;
    }
}

// Tabloyu Doldur
function renderTable(products) {
    tableBody.innerHTML = '';
    if (products.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">Henüz ürün eklenmemiş.</td></tr>`;
        return;
    }
    
    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>#${product.id}</td>
            <td><strong>${product.name}</strong></td>
            <td>${product.category || '-'}</td>
            <td>
                <span style="color: ${product.quantity < 5 ? 'var(--danger-color)' : 'inherit'}">
                    ${product.quantity}
                </span>
            </td>
            <td>${product.price.toFixed(2)} ₺</td>
            <td>
                <button class="btn action-btn edit-btn" onclick="editProduct(${product.id})">Düzenle</button>
                <button class="btn action-btn delete-btn" onclick="deleteProduct(${product.id})">Sil</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Form Gönderimi (Ekle / Güncelle)
productForm.onsubmit = async (e) => {
    e.preventDefault();
    
    const id = document.getElementById('productId').value;
    const productData = {
        name: document.getElementById('name').value,
        category: document.getElementById('category').value,
        quantity: parseInt(document.getElementById('quantity').value),
        price: parseFloat(document.getElementById('price').value)
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}/${id}` : `${API_URL}/`;

    try {
        await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(productData)
        });
        modal.style.display = 'none';
        fetchProducts();
    } catch (error) {
        console.error('Hata:', error);
        alert('Kayıt sırasında bir hata oluştu.');
    }
}

// Ürün Sil
async function deleteProduct(id) {
    if(confirm('Bu ürünü silmek istediğinize emin misiniz?')) {
        try {
            await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
            fetchProducts();
        } catch (error) {
            console.error('Hata:', error);
            alert('Silme sırasında hata oluştu.');
        }
    }
}

// Ürün Düzenle
async function editProduct(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`);
        const product = await response.json();
        
        document.getElementById('productId').value = product.id;
        document.getElementById('name').value = product.name;
        document.getElementById('category').value = product.category;
        document.getElementById('quantity').value = product.quantity;
        document.getElementById('price').value = product.price;
        
        modalTitle.textContent = 'Ürünü Düzenle';
        modal.style.display = 'flex';
    } catch (error) {
        console.error('Hata:', error);
    }
}

document.addEventListener('DOMContentLoaded', fetchProducts);
