/* Satya Sai Baba Auto Electrical Works - Main JS */
AOS.init({ duration: 700, once: true, offset: 60 });

const mainNav = document.getElementById('mainNav');
if (mainNav) {
  window.addEventListener('scroll', () => mainNav.classList.toggle('scrolled', window.scrollY > 60));
}

setTimeout(() => {
  document.querySelectorAll('.flash-msg').forEach(el => bootstrap.Alert.getOrCreateInstance(el).close());
}, 5000);

function showNotif(title, msg) {
  let container = document.getElementById('notification-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'notification-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = 'notif-toast';
  toast.innerHTML = `<div class="d-flex align-items-center gap-2 mb-1"><span class="live-dot"></span><strong style="font-family:var(--font-display);font-size:14px">${title}</strong><button onclick="this.closest('.notif-toast').remove()" style="background:none;border:none;color:#666;margin-left:auto;cursor:pointer;font-size:16px">&times;</button></div><div style="font-size:13px;color:var(--text-light)">${msg}</div>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 7000);
}

try {
  const socket = io();
  socket.on('inventory_update', data => {
    const el = document.querySelector(`[data-stock-id="${data.item_type}-${data.item_id}"]`);
    if (el) el.textContent = data.quantity_after;
    if (data.quantity_after < 3) showNotif('Low Stock Alert', `Item #${data.item_id} has only ${data.quantity_after} left!`);
  });
  socket.on('new_booking', data => {
    if (window.location.pathname.startsWith('/admin')) showNotif('New Booking', `${data.customer} booked for ${data.date}`);
  });
  socket.on('new_inquiry', data => {
    if (window.location.pathname.startsWith('/admin')) showNotif('New Inquiry', `${data.name}: ${data.subject || 'New message'}`);
  });
  if (window.location.pathname.startsWith('/admin')) socket.emit('join_admin');
} catch(e) { console.warn('Socket unavailable'); }

const searchInput = document.getElementById('productSearch');
if (searchInput) {
  let timer, box;
  searchInput.addEventListener('input', function() {
    clearTimeout(timer);
    const q = this.value.trim();
    if (q.length < 2) { if(box){box.remove();box=null;} return; }
    timer = setTimeout(async () => {
      const res = await fetch(`/api/products/search?q=${encodeURIComponent(q)}`);
      const items = await res.json();
      if(box){box.remove();}
      if(!items.length) return;
      box = document.createElement('div');
      box.className = 'search-suggestions';
      items.forEach(item => {
        const d = document.createElement('div');
        d.className = 'search-item';
        d.innerHTML = `<div><div class="search-item-name">${item.name}</div><div class="search-item-part">${item.brand_name||''} ${item.part_number?'· '+item.part_number:''}</div></div>${item.price?`<div class="search-item-price">₹${parseFloat(item.price).toLocaleString('en-IN')}</div>`:''}`;
        d.addEventListener('mousedown', () => window.location.href=`/products?q=${encodeURIComponent(item.name)}`);
        box.appendChild(d);
      });
      searchInput.closest('.search-wrapper').appendChild(box);
    }, 300);
  });
  searchInput.addEventListener('blur', () => setTimeout(() => {if(box){box.remove();box=null;}}, 200));
}

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target, target = parseInt(el.dataset.count);
      let start = null;
      const step = ts => {
        if(!start) start=ts;
        const p = Math.min((ts-start)/1500,1);
        el.textContent = Math.floor(p*target).toLocaleString('en-IN')+(el.dataset.suffix||'');
        if(p<1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      observer.unobserve(el);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('[data-count]').forEach(el => observer.observe(el));

const bookingDate = document.getElementById('booking_date');
if (bookingDate) {
  const tom = new Date(); tom.setDate(tom.getDate()+1);
  bookingDate.min = tom.toISOString().split('T')[0];
  const max = new Date(); max.setDate(max.getDate()+30);
  bookingDate.max = max.toISOString().split('T')[0];
}

document.querySelectorAll('.btn-delete').forEach(btn => {
  btn.addEventListener('click', e => { if(!confirm('Delete this item?')) e.preventDefault(); });
});
