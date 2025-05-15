// Dashboard logic for owner - English labels
let revenueChart, bookingsChart, statusChart;

function formatPrice(value) {
    if (!value) return '0₫';
    return Number(value).toLocaleString('en-US') + '₫';
}

function destroyCharts() {
    if (revenueChart) { revenueChart.destroy(); revenueChart = null; }
    if (bookingsChart) { bookingsChart.destroy(); bookingsChart = null; }
    if (statusChart) { statusChart.destroy(); statusChart = null; }
}

function loadHotelDashboard(hotelId, hotelName) {
    fetch(`/api/hotel/${hotelId}/dashboard`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('totalHotels').textContent = hotelName || '1';
            document.getElementById('totalRooms').textContent = data.total_rooms || 0;
            document.getElementById('todayBookings').textContent = data.today_bookings || 0;
            document.getElementById('totalBookings').textContent = data.total_bookings || 0;
            document.getElementById('totalRevenue').textContent = formatPrice(data.total_revenue || 0);
            document.getElementById('monthlyRevenue').textContent = formatPrice(data.monthly_revenue || 0);

            // Update hotel buttons with data-hotel-id
            const hotelBtns = document.querySelectorAll('#ownerHotelList .hotel-btn');
            hotelBtns.forEach(btn => {
                if (btn.textContent === hotelName) {
                    btn.setAttribute('data-hotel-id', hotelId);
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // Draw charts
            destroyCharts();
            // Revenue by Month
            const revenueCtx = document.getElementById('revenueChart').getContext('2d');
            revenueChart = new Chart(revenueCtx, {
                type: 'line',
                data: {
                    labels: data.charts.revenue.labels,
                    datasets: [{
                        label: 'Revenue',
                        data: data.charts.revenue.data,
                        borderColor: '#1976d2',
                        backgroundColor: 'rgba(25, 118, 210, 0.1)',
                        fill: true,
                        tension: 0.2
                    }]
                },
                options: {
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
            // Bookings by Month
            const bookingsCtx = document.getElementById('bookingsChart').getContext('2d');
            bookingsChart = new Chart(bookingsCtx, {
                type: 'bar',
                data: {
                    labels: data.charts.bookings.labels,
                    datasets: [{
                        label: 'Bookings',
                        data: data.charts.bookings.data,
                        backgroundColor: '#43a047'
                    }]
                },
                options: {
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
            // Booking Status Rate
            const statusCtx = document.getElementById('statusChart').getContext('2d');
            statusChart = new Chart(statusCtx, {
                type: 'pie',
                data: {
                    labels: ['Success', 'Pending', 'Failed'],
                    datasets: [{
                        data: data.charts.status.data,
                        backgroundColor: ['#43a047', '#fbc02d', '#e53935']
                    }]
                },
                options: {
                    plugins: { legend: { position: 'bottom' } }
                }
            });

            // Load payment history for this hotel
            loadPaymentHistory(hotelId);
        })
        .catch(err => console.error('Error loading hotel dashboard:', err));
}

function loadPaymentHistory(hotelId) {
    const tableWrapper = document.getElementById('paymentHistoryTableWrapper');
    if (!tableWrapper) {
        console.error('Payment history table wrapper not found');
        return;
    }

    // Show loading state
    tableWrapper.innerHTML = '<div class="loading">Loading payment history...</div>';

    fetch(`/api/hotel/${hotelId}/payments`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load payment history');
            }
            return response.json();
        })
        .then(data => {
            if (!data.payments || data.payments.length === 0) {
                tableWrapper.innerHTML = '<div class="no-data">No payment history available</div>';
                return;
            }

            const table = document.createElement('table');
            table.className = 'payment-history-table';

            // Create table header
            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th>Payment ID</th>
                    <th>Payer</th>
                    <th>Amount</th>
                    <th>Room Type</th>
                    <th>Date</th>
                    <th>Status</th>
                </tr>
            `;
            table.appendChild(thead);

            // Create table body
            const tbody = document.createElement('tbody');
            data.payments.forEach(payment => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${payment.payment_id}</td>
                    <td>${payment.payer_name}</td>
                    <td>${formatPrice(payment.amount)}</td>
                    <td>${payment.room_type}</td>
                    <td>${payment.created_at}</td>
                    <td><span class="status-badge ${payment.status.toLowerCase()}">${payment.status}</span></td>
                `;
                tbody.appendChild(tr);
            });
            table.appendChild(tbody);

            // Clear and append table
            tableWrapper.innerHTML = '';
            tableWrapper.appendChild(table);
        })
        .catch(error => {
            console.error('Error loading payment history:', error);
            tableWrapper.innerHTML = '<div class="error">Failed to load payment history. Please try again later.</div>';
        });
}

function loadPaymentHistoryHotelListAndDefault() {
    // Lấy danh sách khách sạn owner sở hữu
    fetch('/api/owner/dashboard')
        .then(res => res.json())
        .then(data => {
            const hotelList = data.hotels || [];
            const listDiv = document.getElementById('paymentHistoryHotelList');
            if (!listDiv) return;
            if (hotelList.length === 0) {
                listDiv.innerHTML = '<div class="no-data">No hotels found.</div>';
                document.getElementById('paymentHistoryTableWrapper').innerHTML = '';
                return;
            }
            // Render nút
            listDiv.innerHTML = hotelList.map((h, idx) =>
                `<button class="hotel-btn${idx === 0 ? ' active' : ''}" data-hotel-id="${h.hotel_id}">${h.hotel_name}</button>`
            ).join('');
            // Gán sự kiện click
            Array.from(listDiv.querySelectorAll('.hotel-btn')).forEach(btn => {
                btn.onclick = function () {
                    Array.from(listDiv.querySelectorAll('.hotel-btn')).forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    const hotelId = btn.getAttribute('data-hotel-id');
                    if (hotelId) loadPaymentHistory(hotelId);
                };
            });
            // Tự động load payment history khách sạn đầu tiên
            const firstHotelId = hotelList[0].hotel_id;
            if (firstHotelId) loadPaymentHistory(firstHotelId);
        })
        .catch(err => {
            const listDiv = document.getElementById('paymentHistoryHotelList');
            if (listDiv) listDiv.innerHTML = '<div class="error">Error loading hotel list.</div>';
        });
}

// Sửa switchSection để gọi hàm trên khi vào tab hotel-rooms
const _oldSwitchSection = window.switchSection;
window.switchSection = function (sectionId) {
    _oldSwitchSection(sectionId);
    if (sectionId === 'hotel-rooms') {
        loadPaymentHistoryHotelListAndDefault();
    }
};

// Tự động load dashboard đầu tiên khi vào trang (nếu là owner)
document.addEventListener('DOMContentLoaded', function () {
    const dashboardSection = document.getElementById('dashboard');
    if (!dashboardSection) return;
    // Nếu có nút khách sạn, tự động click vào nút đầu tiên
    const hotelBtns = document.querySelectorAll('#ownerHotelList .hotel-btn');
    if (hotelBtns.length > 0) {
        hotelBtns[0].click();
    }
}); 