// ===============================
// EliteLance Theme Toggle
// ===============================

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("theme-toggle");

    // Load saved theme
    if (localStorage.getItem("theme") === "light") {
        document.documentElement.classList.remove("dark");
    } else {
        document.documentElement.classList.add("dark");
    }

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            if (document.documentElement.classList.contains("dark")) {
                document.documentElement.classList.remove("dark");
                localStorage.setItem("theme", "light");
            } else {
                document.documentElement.classList.add("dark");
                localStorage.setItem("theme", "dark");
            }
        });
    }
});