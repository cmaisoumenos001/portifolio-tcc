function openLogoutModal() {
  document.getElementById("modal-logout").style.display = "flex";
}

function closeModal() {
  document.getElementById("modal-logout").style.display = "none";
}

function confirmLogout() {
  window.location.href = "/logout";
}

function Senha(id) {
  const senha = document.getElementById(id);

  if (!senha) return;

  senha.type = senha.type === "password" ? "text" : "password";
}
