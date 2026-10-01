// Mock Product Data & Inventory Management for The Aura Boutique
const defaultProducts = [
    // ================= SKIN CARE (12 Products) =================
    {
        id: 1,
        name: "Hyaluronic Acid 2% + B5 Hydration Serum",
        brand: "The Ordinary",
        category: "Skin",
        price: 799,
        stock: 15,
        description: "Multi-depth hydration formula combining ultra-pure vegan hyaluronic acid with provitamin B5.",
        image: "assets/products/prod_1.jpg"
    },
    {
        id: 2,
        name: "10% Niacinamide Clarifying Serum",
        brand: "Plum",
        category: "Skin",
        price: 599,
        stock: 12,
        description: "Blemish and oil-balancing serum that visibly refines enlarged pores and calms inflammation.",
        image: "assets/products/prod_2.jpg"
    },
    {
        id: 3,
        name: "Vitamin C 16% Radiance Elixir",
        brand: "Minimalist",
        category: "Skin",
        price: 699,
        stock: 0,
        description: "Stabilized Ethyl Ascorbic Acid with ferulic acid to illuminate skin and fade hyperpigmentation.",
        image: "assets/products/prod_3.jpg"
    },
    {
        id: 4,
        name: "Salicylic Acid Gentle Exfoliating Cleanser",
        brand: "CeraVe",
        category: "Skin",
        price: 1299,
        stock: 20,
        description: "Formulated with essential ceramides to smooth rough skin texture while preserving the moisture barrier.",
        image: "assets/products/prod_4.jpg"
    },
    {
        id: 5,
        name: "Gentle Foaming Hydrating Cleanser",
        brand: "Cetaphil",
        category: "Skin",
        price: 549,
        stock: 18,
        description: "Hypoallergenic, dermatologist-tested micellar foam that washes away impurities without tightness.",
        image: "assets/products/prod_5.jpg"
    },
    {
        id: 6,
        name: "Ceramide Barrier Strengthening Cream",
        brand: "Dr. Jart+",
        category: "Skin",
        price: 2150,
        stock: 8,
        description: "Deeply moisturizing barrier cream powered by 5-Cera Complex to shield against dehydration.",
        image: "assets/products/prod_6.jpg"
    },
    {
        id: 7,
        name: "UV Water-Light Essence SPF 50+ PA++++",
        brand: "Bioré",
        category: "Skin",
        price: 990,
        stock: 25,
        description: "Invisible micro-defense photoprotection that melts instantly onto skin with zero white cast.",
        image: "assets/products/prod_7.jpg"
    },
    {
        id: 8,
        name: "Ultra-Hydrating Squalane Cloud Toner",
        brand: "Kiehl's",
        category: "Skin",
        price: 1850,
        stock: 10,
        description: "Nourishing milky toner enriched with glacial glycoproteins to tone and prepare skin for actives.",
        image: "assets/products/prod_8.jpg"
    },
    {
        id: 9,
        name: "Clinical 0.5% Encapsulated Retinol Serum",
        brand: "Paula's Choice",
        category: "Skin",
        price: 2400,
        stock: 6,
        description: "Time-released micro-retinol formulated with soothing peptides to firm and accelerate renewal.",
        image: "assets/products/prod_9.jpg"
    },
    {
        id: 10,
        name: "Purifying French Rose Kaolin Clay Mask",
        brand: "Origins",
        category: "Skin",
        price: 1650,
        stock: 9,
        description: "Rich mineral-packed clay treatment that draws out deep pore debris and balances surface sheen.",
        image: "assets/products/prod_10.jpg"
    },
    {
        id: 11,
        name: "Peptide & Caffeine Awakening Eye Cream",
        brand: "Sunday Riley",
        category: "Skin",
        price: 2850,
        stock: 4,
        description: "Luminizing orbital treatment that dramatically reduces fluid puffiness and dark circadian circles.",
        image: "assets/products/prod_11.jpg"
    },
    {
        id: 12,
        name: "Berry Peptide Lip Sleeping Mask",
        brand: "Laneige",
        category: "Skin",
        price: 600,
        stock: 30,
        description: "Nutritive balm with Moisture Wrap technology to dissolve dead skin cells and lock in suppleness.",
        image: "assets/products/prod_12.jpg"
    },

    // ================= HAIR CARE (12 Products) =================
    {
        id: 13,
        name: "No. 4 Bond Maintenance Repair Shampoo",
        brand: "Olaplex",
        category: "Hair",
        price: 2950,
        stock: 14,
        description: "Patented bond-building chemistry that relinks broken disulfide bonds from chemical styling.",
        image: "assets/products/prod_13.jpg"
    },
    {
        id: 14,
        name: "Hydrating Botanical Moisture Shampoo",
        brand: "Moroccanoil",
        category: "Hair",
        price: 2100,
        stock: 16,
        description: "Infused with antioxidant-rich argan oil and red algae to revitalize moisture balance in parched hair.",
        image: "assets/products/prod_14.jpg"
    },
    {
        id: 15,
        name: "No-Frizz Weightless Smoothing Conditioner",
        brand: "Living Proof",
        category: "Hair",
        price: 2450,
        stock: 8,
        description: "Powered by Healthy Hair Molecule technology to block atmospheric humidity and eliminate flyaways.",
        image: "assets/products/prod_15.jpg"
    },
    {
        id: 16,
        name: "Discipline Keratin Deep-Repair Mask",
        brand: "Kérastase",
        category: "Hair",
        price: 3400,
        stock: 5,
        description: "Cationic polymer infusion that seals damaged hair cuticles and provides fluid movement.",
        image: "assets/products/prod_16.jpg"
    },
    {
        id: 17,
        name: "Professional Glossing Argan Hair Serum",
        brand: "Streax",
        category: "Hair",
        price: 450,
        stock: 22,
        description: "Lightweight polishing serum with macadamia oil that detangles strands and imparts mirror shine.",
        image: "assets/products/prod_17.jpg"
    },
    {
        id: 18,
        name: "Multi-Peptide Scalp Density Serum",
        brand: "The Ordinary",
        category: "Hair",
        price: 1799,
        stock: 7,
        description: "Concentrated leave-in scalp therapy designed to promote visible density, thickness, and follicle health.",
        image: "assets/products/prod_18.jpg"
    },
    {
        id: 19,
        name: "Rosemary & Biotin Root Strengthening Oil",
        brand: "Mielle Organics",
        category: "Hair",
        price: 1250,
        stock: 19,
        description: "Over 30 essential botanical oils formulated to invigorate scalp micro-circulation and length retention.",
        image: "assets/products/prod_19.jpg"
    },
    {
        id: 20,
        name: "Coconut & Shea Butter Curl Activator Cream",
        brand: "Cantu",
        category: "Hair",
        price: 890,
        stock: 11,
        description: "Defines natural curl texture, delivers touchable bounce, and seals in essential lipid moisture.",
        image: "assets/products/prod_20.jpg"
    },
    {
        id: 21,
        name: "Farewell Frizz Milk Leave-In Conditioner",
        brand: "Briogeo",
        category: "Hair",
        price: 2200,
        stock: 0,
        description: "Nutritive spray infused with rosehip and coconut oil to detangle and protect against styling stress.",
        image: "assets/products/prod_21.jpg"
    },
    {
        id: 22,
        name: "Thermal Recovery 450°F Heat Defense Spray",
        brand: "TRESemmé",
        category: "Hair",
        price: 499,
        stock: 35,
        description: "Heat-activated barrier spray that shields hair fibers from thermal iron tools up to 230°C.",
        image: "assets/products/prod_22.jpg"
    },
    {
        id: 23,
        name: "Physiological Anti-Dandruff pH 5.5 Shampoo",
        brand: "Sebamed",
        category: "Hair",
        price: 950,
        stock: 12,
        description: "Mild active wash with Piroctone Olamine to soothe itchy scalp microflora and flakes.",
        image: "assets/products/prod_23.jpg"
    },
    {
        id: 24,
        name: "Avocado Nourish Deep Conditioning Mask",
        brand: "Plum",
        category: "Hair",
        price: 650,
        stock: 15,
        description: "Rich butter formulation packed with monounsaturated lipids to repair split ends and cuticle roughness.",
        image: "assets/products/prod_24.jpg"
    },

    // ================= MAKEUP (14 Products) =================
    {
        id: 25,
        name: "Luminous Silk Oil-Free Liquid Foundation",
        brand: "Giorgio Armani",
        category: "Makeup",
        price: 4900,
        stock: 10,
        description: "Micro-fil technology delivers weightless, buildable couture coverage with a flawless satin glow.",
        image: "assets/products/prod_25.jpg"
    },
    {
        id: 26,
        name: "Radiant Creamy Full-Coverage Concealer",
        brand: "NARS",
        category: "Makeup",
        price: 2800,
        stock: 15,
        description: "Botanical-infused formula that blurs fine lines, camouflages redness, and illuminates for 16 hours.",
        image: "assets/products/prod_26.jpg"
    },
    {
        id: 27,
        name: "Soft Pinch Dewy Liquid Cheek Blush",
        brand: "Rare Beauty",
        category: "Makeup",
        price: 2400,
        stock: 8,
        description: "Featherlight liquid blush that melts into bare skin or foundation for an effortless luminous flush.",
        image: "assets/products/prod_27.jpg"
    },
    {
        id: 28,
        name: "Ambient Lighting Micro-Glow Powder Blush",
        brand: "Hourglass",
        category: "Makeup",
        price: 3950,
        stock: 6,
        description: "Photoluminescent technology creates multidimensional depth and seamless diffused color payoff.",
        image: "assets/products/prod_28.jpg"
    },
    {
        id: 29,
        name: "Matte Revolution Nude Lipstick (Pillow Talk)",
        brand: "Charlotte Tilbury",
        category: "Makeup",
        price: 3500,
        stock: 14,
        description: "Universal cashmere-finish nude pink lipstick formulated with 3D glowing pigments and orchid extract.",
        image: "assets/products/prod_29.jpg"
    },
    {
        id: 30,
        name: "Retro Matte Velvet Blue-Red Lipstick (Ruby Woo)",
        brand: "MAC",
        category: "Makeup",
        price: 2150,
        stock: 20,
        description: "High-voltage long-wearing vivid crimson red that delivers an iconic non-drying matte finish.",
        image: "assets/products/prod_30.jpg"
    },
    {
        id: 31,
        name: "Gloss Bomb Universal Lip Luminizer",
        brand: "Fenty Beauty",
        category: "Makeup",
        price: 1900,
        stock: 18,
        description: "Explosive cushiony shine loaded with conditioning shea butter and a peach-vanilla scent.",
        image: "assets/products/prod_31.jpg"
    },
    {
        id: 32,
        name: "Lip Cheat Precision Velvet Lip Contour",
        brand: "Charlotte Tilbury",
        category: "Makeup",
        price: 2200,
        stock: 12,
        description: "Waterproof, glide-on liner that redefines lip shape and prevents lipstick bleed for up to 6 hours.",
        image: "assets/products/prod_32.jpg"
    },
    {
        id: 33,
        name: "Lash Paradise Feathery Volume Mascara",
        brand: "L'Oréal Paris",
        category: "Makeup",
        price: 799,
        stock: 28,
        description: "Soft undulating brush coats lashes in carbon-black pigments for dramatic length and lift.",
        image: "assets/products/prod_33.jpg"
    },
    {
        id: 34,
        name: "Tattoo Studio 24H Waterproof Liquid Eyeliner",
        brand: "Maybelline",
        category: "Makeup",
        price: 499,
        stock: 32,
        description: "Fade-resistant micro-felt tip produces sharp, smudge-proof lines that resist sweat and humidity.",
        image: "assets/products/prod_34.jpg"
    },
    {
        id: 35,
        name: "Empowered 18-Pan High-Impact Eyeshadow Palette",
        brand: "Huda Beauty",
        category: "Makeup",
        price: 5400,
        stock: 5,
        description: "Curated spectrum of buttery mattes, reflective gels, and metallic foils for bespoke eye looks.",
        image: "assets/products/prod_35.jpg"
    },
    {
        id: 36,
        name: "Killawatt Freestyle Holographic Highlighter",
        brand: "Fenty Beauty",
        category: "Makeup",
        price: 3200,
        stock: 7,
        description: "Weightless cream-powder hybrid highlighter that blends effortlessly on cheekbones with fine sheen.",
        image: "assets/products/prod_36.jpg"
    },
    {
        id: 37,
        name: "All Nighter Long-Wear Setting Spray",
        brand: "Urban Decay",
        category: "Makeup",
        price: 2900,
        stock: 11,
        description: "Patented Temperature Control Technology lowers makeup temperature to lock looks for 16 hours.",
        image: "assets/products/prod_37.jpg"
    },
    {
        id: 38,
        name: "Airbrush Flawless Finish Micro-Powder",
        brand: "Charlotte Tilbury",
        category: "Makeup",
        price: 4100,
        stock: 0,
        description: "Breathable micro-powder that optically blurs pores, softens lines, and controls shine with almond wax.",
        image: "assets/products/prod_38.jpg"
    }
];

// Smart LocalStorage Initialization & Migration
let storedInventory = JSON.parse(localStorage.getItem('aura_inventory'));
let inventory = [];

if (!storedInventory || storedInventory.length <= 12 || !storedInventory[0].image || !storedInventory[0].description) {
    // Legacy inventory detected (old 12 items without images/descriptions): Migrate to full 38 product catalog
    inventory = [...defaultProducts];
    if (storedInventory && storedInventory.length > 0) {
        // Retain any custom products added dynamically by user/seller (id > 10000)
        const customAdded = storedInventory.filter(p => p.id > 10000);
        if (customAdded.length > 0) {
            inventory = [...customAdded, ...inventory];
        }
    }
    localStorage.setItem('aura_inventory', JSON.stringify(inventory));
} else {
    inventory = storedInventory;
}

let cart = JSON.parse(localStorage.getItem('aura_cart')) || [];
let orders = JSON.parse(localStorage.getItem('aura_orders')) || [];
let inventoryLogs = JSON.parse(localStorage.getItem('aura_inventory_logs')) || [];

// DOM Elements
const productsGrid = document.getElementById('products-grid');
const filterBtns = document.querySelectorAll('.filter-btn');
const cartBtn = document.getElementById('cart-btn');
const closeCartBtn = document.getElementById('close-cart');
const cartOverlay = document.getElementById('cart-overlay');
const cartSidebar = document.getElementById('cart-sidebar');
const cartItemsContainer = document.getElementById('cart-items');
const cartCount = document.getElementById('cart-count');
const cartTotalPrice = document.getElementById('cart-total-price');
const navbar = document.getElementById('navbar');

// Scroll Effect for Navbar
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Render Products with Image on Top & Luxury Card Structure
function renderProducts(category = 'All') {
    productsGrid.innerHTML = '';
    
    const filteredProducts = category === 'All' 
        ? inventory 
        : inventory.filter(p => p.category === category);
        
    if (filteredProducts.length === 0) {
        productsGrid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted); font-size: 16px;">
                No formulations available in this category currently.
            </div>
        `;
        return;
    }
        
    filteredProducts.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        let stockBadge = '';
        let actionBtn = '';
        let deleteBtn = '';
        
        if (product.stock > 0) {
            stockBadge = `<div class="stock-badge">In Stock: ${product.stock}</div>`;
            actionBtn = `<button class="add-to-cart" onclick="addToCart(${product.id})">Add to Cart</button>`;
        } else {
            stockBadge = `<div class="stock-badge out-of-stock">Out of Stock</div>`;
            actionBtn = `<button class="add-to-cart out-of-stock-btn" disabled>Out of Stock</button>`;
            deleteBtn = `<button class="delete-product-btn" onclick="deleteProduct(${product.id})">Remove from Catalog</button>`;
        }
        
        const fallbackImg = product.category === 'Hair' 
            ? 'assets/aura_haircare.png' 
            : (product.category === 'Makeup' ? 'assets/aura_makeup.png' : 'assets/aura_skincare.png');
            
        const imgSrc = product.image || `assets/products/prod_${product.id}.jpg`;
        
        card.innerHTML = `
            <div class="product-image-wrap">
                <img src="${imgSrc}" alt="${product.name}" class="product-img" loading="lazy" onerror="this.onerror=null; this.src='${fallbackImg}';">
                ${stockBadge}
            </div>
            <div class="product-info-wrap">
                <div class="product-meta-header">
                    <span class="product-category">${product.category} Care</span>
                    <span class="product-brand">${product.brand}</span>
                </div>
                <h4 class="product-name" title="${product.name}">${product.name}</h4>
                <p class="product-desc">${product.description || 'Clinical-grade luxury formulation designed for optimal bioavailability.'}</p>
                <div class="product-price-row">
                    <span class="product-price">₹${product.price}</span>
                    ${actionBtn}
                </div>
                ${deleteBtn}
            </div>
        `;
        productsGrid.appendChild(card);
    });
}

function deleteProduct(id) {
    if (confirm("Are you sure you want to completely remove this out-of-stock product from the catalog?")) {
        inventory = inventory.filter(p => p.id !== id);
        localStorage.setItem('aura_inventory', JSON.stringify(inventory));
        
        // Find active filter
        const activeBtn = document.querySelector('.filter-btn.active');
        const activeCat = activeBtn ? activeBtn.dataset.filter : 'All';
        renderProducts(activeCat);
    }
}

// Filter Logic without Page Refresh
filterBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        filterBtns.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        renderProducts(e.target.dataset.filter);
    });
});

// Category Cards Logic
document.querySelectorAll('.category-card').forEach(card => {
    card.addEventListener('click', () => {
        const cat = card.dataset.category;
        
        // Scroll smoothly to shop
        document.getElementById('shop').scrollIntoView({ behavior: 'smooth' });
        
        // Update filter button states
        filterBtns.forEach(b => b.classList.remove('active'));
        const activeBtn = Array.from(filterBtns).find(b => b.dataset.filter === cat);
        if (activeBtn) activeBtn.classList.add('active');
        
        renderProducts(cat);
    });
});

// Cart Logic
function addToCart(productId) {
    const product = inventory.find(p => p.id === productId);
    if (!product) return;
    
    const existingCartItem = cart.find(item => item.product.id === productId);
    const currentQty = existingCartItem ? existingCartItem.quantity : 0;
    
    if (currentQty < product.stock) {
        if (existingCartItem) {
            existingCartItem.quantity += 1;
        } else {
            cart.push({ product: product, quantity: 1 });
        }
        
        updateCart();
        
        // Flash cart icon
        cartCount.style.transform = 'scale(1.4)';
        setTimeout(() => cartCount.style.transform = 'scale(1)', 200);
        
        // Open cart sidebar
        openCart();
    } else {
        alert("Cannot add more to cart. Maximum available live stock reached for this formulation.");
    }
}

function incrementCartItem(productId) {
    addToCart(productId);
}

function decrementCartItem(productId) {
    const index = cart.findIndex(item => item.product.id === productId);
    if (index > -1) {
        cart[index].quantity -= 1;
        if (cart[index].quantity <= 0) {
            cart.splice(index, 1);
        }
        updateCart();
    }
}

function updateCart() {
    cartItemsContainer.innerHTML = '';
    let total = 0;
    let totalItems = 0;
    
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p style="color:var(--text-muted); text-align:center; margin-top:50px;">Your cart is currently empty.</p>';
    } else {
        cart.forEach(item => {
            total += item.product.price * item.quantity;
            totalItems += item.quantity;
            
            const cartItem = document.createElement('div');
            cartItem.className = 'cart-item';
            
            const isMaxStock = item.quantity >= item.product.stock;
            const fallbackImg = item.product.category === 'Hair' 
                ? 'assets/aura_haircare.png' 
                : (item.product.category === 'Makeup' ? 'assets/aura_makeup.png' : 'assets/aura_skincare.png');
            const imgSrc = item.product.image || `assets/products/prod_${item.product.id}.jpg`;
            
            cartItem.innerHTML = `
                <div style="display:flex; gap:12px; align-items:center; width:100%;">
                    <img src="${imgSrc}" style="width:50px; height:50px; object-fit:cover; border-radius:6px; border:1px solid var(--border-light);" onerror="this.src='${fallbackImg}';">
                    <div class="cart-item-info" style="flex:1;">
                        <h4 style="margin:0 0 3px 0; font-size:13.5px; line-height:1.3;">${item.product.name}</h4>
                        <p style="margin:0 0 4px 0; font-size:11.5px; color:var(--text-muted);">${item.product.brand}</p>
                        <div class="cart-item-price" style="font-size:13px; font-weight:700;">₹${item.product.price}</div>
                        <div class="cart-item-qty">
                            <button class="qty-btn" onclick="decrementCartItem(${item.product.id})">-</button>
                            <span style="font-size:13px; font-weight:bold; min-width:20px; text-align:center;">${item.quantity}</span>
                            <button class="qty-btn" onclick="incrementCartItem(${item.product.id})" ${isMaxStock ? 'disabled' : ''}>+</button>
                        </div>
                    </div>
                    <div class="cart-item-price" style="font-size:14px; font-weight:700;">₹${item.product.price * item.quantity}</div>
                </div>
            `;
            cartItemsContainer.appendChild(cartItem);
        });
    }
    
    cartCount.innerText = totalItems;
    cartTotalPrice.innerText = '₹' + total;
    localStorage.setItem('aura_cart', JSON.stringify(cart));
}

// UI Modals & Navigation
const checkoutBtn = document.querySelector('.checkout-btn');
const checkoutModal = document.getElementById('checkout-modal');
const closeCheckoutBtn = document.getElementById('close-checkout');
const checkoutForm = document.getElementById('checkout-form');
const checkoutFinalPrice = document.getElementById('checkout-final-price');
const successModal = document.getElementById('success-modal');
const continueShoppingBtn = document.getElementById('continue-shopping');
const paymentIdDisplay = document.getElementById('payment-id-display');

// Seller & Orders Modals
const navSeller = document.getElementById('nav-seller');
const sellerModal = document.getElementById('seller-modal');
const closeSellerBtn = document.getElementById('close-seller');
const addProductForm = document.getElementById('add-product-form');

const restockForm = document.getElementById('restock-form');
const restockProdId = document.getElementById('restock-prod-id');
const restockAmount = document.getElementById('restock-amount');

const navOrders = document.getElementById('nav-orders');
const ordersModal = document.getElementById('orders-modal');
const closeOrdersBtn = document.getElementById('close-orders');
const ordersList = document.getElementById('orders-list');

// Random ID Generator
function generateId() {
    return 'AURA-TXN-' + Math.random().toString(36).substr(2, 9).toUpperCase();
}

function openCart() {
    cartOverlay.classList.add('active');
    cartSidebar.classList.add('active');
}

function closeCart() {
    cartOverlay.classList.remove('active');
    cartSidebar.classList.remove('active');
}

// Checkout Flow
checkoutBtn.addEventListener('click', () => {
    if (cart.length === 0) {
        alert("Your cart is empty. Please select a formulation from our boutique.");
        return;
    }
    closeCart();
    checkoutFinalPrice.innerText = cartTotalPrice.innerText;
    checkoutModal.classList.add('active');
});

closeCheckoutBtn.addEventListener('click', () => {
    checkoutModal.classList.remove('active');
});

checkoutForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Decrement stock for purchased items
    cart.forEach(cartItem => {
        const invItem = inventory.find(p => p.id === cartItem.product.id);
        if (invItem && invItem.stock > 0) {
            invItem.stock -= cartItem.quantity;
        }
    });
    
    // Save updated inventory
    localStorage.setItem('aura_inventory', JSON.stringify(inventory));
    
    // Generate secure Payment ID
    const paymentId = generateId();
    paymentIdDisplay.innerText = paymentId;
    
    // Create Order Object
    const newOrder = {
        id: paymentId,
        date: new Date().toLocaleDateString() + ' ' + new Date().toLocaleTimeString(),
        items: cart.map(i => `${i.product.name} (x${i.quantity})`),
        total: cartTotalPrice.innerText
    };
    
    // Save to LocalStorage
    orders.unshift(newOrder);
    localStorage.setItem('aura_orders', JSON.stringify(orders));
    
    checkoutModal.classList.remove('active');
    successModal.classList.add('active');
    
    // Clear Cart
    cart = [];
    updateCart();
    checkoutForm.reset();
    
    // Re-render products to show updated live stock
    const activeBtn = document.querySelector('.filter-btn.active');
    const activeCat = activeBtn ? activeBtn.dataset.filter : 'All';
    renderProducts(activeCat);
});

continueShoppingBtn.addEventListener('click', () => {
    successModal.classList.remove('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

cartBtn.addEventListener('click', openCart);
closeCartBtn.addEventListener('click', closeCart);
cartOverlay.addEventListener('click', closeCart);

// Seller Dashboard Logic
navSeller.addEventListener('click', (e) => {
    e.preventDefault();
    
    // Populate restock dropdown
    restockProdId.innerHTML = '';
    inventory.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = `${p.name} - ${p.brand} (Current Stock: ${p.stock})`;
        restockProdId.appendChild(option);
    });
    
    sellerModal.classList.add('active');
});

closeSellerBtn.addEventListener('click', () => {
    sellerModal.classList.remove('active');
});

restockForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const pId = parseInt(restockProdId.value);
    const amount = parseInt(restockAmount.value);
    const recvDate = document.getElementById('restock-recv-date').value;
    const invoiceNo = document.getElementById('restock-invoice-no').value;
    const invoiceDate = document.getElementById('restock-invoice-date').value;
    const vendor = document.getElementById('restock-vendor').value;
    
    const prodIndex = inventory.findIndex(p => p.id === pId);
    if (prodIndex > -1) {
        inventory[prodIndex].stock += amount;
        localStorage.setItem('aura_inventory', JSON.stringify(inventory));
        
        // Log inventory receipt
        const receiptLog = {
            id: 'LOG-' + Date.now(),
            productId: pId,
            productName: inventory[prodIndex].name,
            quantityReceived: amount,
            receivingDate: recvDate,
            invoiceNumber: invoiceNo,
            invoiceDate: invoiceDate,
            vendorName: vendor,
            timestamp: new Date().toISOString()
        };
        inventoryLogs.unshift(receiptLog);
        localStorage.setItem('aura_inventory_logs', JSON.stringify(inventoryLogs));
        
        const activeBtn = document.querySelector('.filter-btn.active');
        const activeCat = activeBtn ? activeBtn.dataset.filter : 'All';
        renderProducts(activeCat);
        
        sellerModal.classList.remove('active');
        restockForm.reset();
        
        alert(`Successfully received ${amount} units of ${inventory[prodIndex].name}!\nInvoice: ${invoiceNo} logged in inventory records.`);
    }
});

addProductForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const cat = document.getElementById('new-prod-cat').value;
    const fallbackImg = cat === 'Hair' 
        ? 'assets/aura_haircare.png' 
        : (cat === 'Makeup' ? 'assets/aura_makeup.png' : 'assets/aura_skincare.png');
        
    const newProduct = {
        id: Date.now(),
        name: document.getElementById('new-prod-name').value,
        brand: document.getElementById('new-prod-brand').value,
        category: cat,
        price: parseInt(document.getElementById('new-prod-price').value),
        stock: parseInt(document.getElementById('new-prod-stock').value),
        description: "Official formulation added via Seller Inventory Management.",
        image: fallbackImg
    };
    
    inventory.unshift(newProduct);
    localStorage.setItem('aura_inventory', JSON.stringify(inventory));
    
    const activeBtn = document.querySelector('.filter-btn.active');
    const activeCat = activeBtn ? activeBtn.dataset.filter : 'All';
    renderProducts(activeCat);
    
    sellerModal.classList.remove('active');
    addProductForm.reset();
    
    alert("New cosmetic product added successfully to the catalog!");
});

// Orders History Logic
navOrders.addEventListener('click', (e) => {
    e.preventDefault();
    renderOrders();
    ordersModal.classList.add('active');
});

closeOrdersBtn.addEventListener('click', () => {
    ordersModal.classList.remove('active');
});

function renderOrders() {
    ordersList.innerHTML = '';
    
    if (orders.length === 0) {
        ordersList.innerHTML = '<p style="color:var(--text-muted); text-align:center; margin-top:20px;">No past order history found.</p>';
        return;
    }
    
    orders.forEach(order => {
        let itemsHtml = order.items.join('<br>');
        
        const orderCard = document.createElement('div');
        orderCard.className = 'order-card';
        orderCard.innerHTML = `
            <div class="order-header">
                <span class="order-id">${order.id}</span>
                <span class="order-date">${order.date}</span>
            </div>
            <div class="order-items">${itemsHtml}</div>
            <div class="order-total">${order.total}</div>
        `;
        ordersList.appendChild(orderCard);
    });
}

// Initial Render
renderProducts('All');
updateCart();
