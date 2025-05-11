// Profile Dropdown
document.addEventListener('DOMContentLoaded', function () {
    const profileButton = document.querySelector('.profile-button');
    const dropdownContent = document.querySelector('.dropdown-content');

    if (profileButton && dropdownContent) {
        profileButton.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdownContent.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (e) {
            if (!profileButton.contains(e.target)) {
                dropdownContent.classList.remove('show');
            }
        });
    }
}); 