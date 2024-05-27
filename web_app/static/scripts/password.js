function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const togglePasswordIcon = document.getElementById('toggle-password-icon');
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    togglePasswordIcon.classList.toggle('fa-eye');
    togglePasswordIcon.classList.toggle('fa-eye-slash');
}