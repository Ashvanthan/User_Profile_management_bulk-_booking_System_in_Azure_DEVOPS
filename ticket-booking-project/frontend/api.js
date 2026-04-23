// ============================================================
//  api.js — Shared API client, auth helpers, utilities
// ============================================================

const API_BASE = "https://sc-ticket-backend-dra9bsc2dqgwehbx.southeastasia-01.azurewebsites.net/api";
// For local dev: const API_BASE = "http://localhost:7071/api";

// ── Auth helpers ──────────────────────────────────────────
const Auth = {
  save(data) {
    localStorage.setItem("token", data.token);
    localStorage.setItem("user", JSON.stringify(data.user));
  },
  clear() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },
  token() { return localStorage.getItem("token"); },
  user() {
    try { return JSON.parse(localStorage.getItem("user")); }
    catch { return null; }
  },
  isLoggedIn() { return !!this.token() && !!this.user(); },
  role() { return this.user()?.role || null; },
  requireLogin() {
    if (!this.isLoggedIn()) { window.location.href = "login.html"; return false; }
    return true;
  },
  requireRole(roles) {
    if (!this.requireLogin()) return false;
    if (!roles.includes(this.role())) { window.location.href = "dashboard.html"; return false; }
    return true;
  },
  logout() {
    this.clear();
    window.location.href = "login.html";
  }
};

// ── API client ────────────────────────────────────────────
const API = {
  async call(endpoint, method = "GET", body = null, auth = true) {
    const headers = { "Content-Type": "application/json" };
    if (auth && Auth.token()) headers["Authorization"] = `Bearer ${Auth.token()}`;

    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);

    try {
      const res = await fetch(`${API_BASE}/${endpoint}`, opts);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
      return data;
    } catch (err) {
      throw err;
    }
  },

  get:    (ep, auth = true) => API.call(ep, "GET", null, auth),
  post:   (ep, body, auth = true) => API.call(ep, "POST", body, auth),
  put:    (ep, body, auth = true) => API.call(ep, "PUT", body, auth),

  // ── Specific endpoints ──
  register:       (d) => API.post("register", d, false),
  verifyOtp:      (d) => API.post("verifyOtp", d, false),
  login:          (d) => API.post("login", d, false),
  getMovies:      (theaterId) => API.get(theaterId ? `getMovies?theaterId=${theaterId}` : "getMovies", false),
  getTheaters:    (city) => API.get(city ? `getTheaters?city=${encodeURIComponent(city)}` : "getTheaters", false),
  bookTicket:     (d) => API.post("bookTicket", d),
  bulkBooking:    (d) => API.post("bulkBooking", d),
  addMovie:       (d) => API.post("addMovie", d),
  addTheater:     (d) => API.post("addTheater", d),
  removeUser:     (d) => API.post("removeUser", d),
  approveCompany: (d) => API.post("approveCompany", d),
  flagTheater:    (d) => API.post("flagTheater", d),
  getProfile:     ()  => API.get("getUserProfile"),
  updateProfile:  (d) => API.put("updateProfile", d),
  deactivate:     ()  => API.post("deactivateAccount", {}),
  getMyBookings:  ()  => API.get("getMyBookings"),
  getPendingAdmins: () => API.get("getPendingAdmins"),
  getAllUsers:     ()  => API.get("getAllUsers"),
  getAllBookings:  ()  => API.get("getAllBookings"),
};

// ── UI utilities ──────────────────────────────────────────
const UI = {
  showAlert(id, msg, type = "error") {
    const el = document.getElementById(id);
    if (!el) return;
    el.className = `alert alert-${type} show`;
    el.textContent = msg;
    if (type !== "error") setTimeout(() => el.classList.remove("show"), 4000);
  },
  hideAlert(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove("show");
  },
  setLoading(btnId, loading) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.disabled = loading;
    btn.innerHTML = loading
      ? `<span class="spinner"></span> Please wait...`
      : btn.dataset.label || btn.textContent;
  },
  renderNav(activePage) {
    const user = Auth.user();
    if (!user) return;
    const navUser = document.getElementById("navUser");
    const navLinks = document.getElementById("navLinks");
    if (navUser) navUser.textContent = `${user.name}`;
    const roleBadge = `<span class="badge-role badge-${user.role}">${user.role}</span>`;
    if (navLinks) {
      let links = `<a href="dashboard.html">Dashboard</a> <a href="booking.html">Movies</a>`;
      if (user.role === "admin" || user.role === "superadmin") links += ` <a href="admin.html">Admin</a>`;
      links += ` <button onclick="Auth.logout()">Logout</button>`;
      navLinks.innerHTML = links;
    }
  },
  formatDate(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
  },
  formatDateTime(iso) {
    if (!iso) return "—";
    return new Date(iso).toLocaleString("en-IN", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
  },
  rupee: (n) => `₹${Number(n).toLocaleString("en-IN")}`
};

// ── Cost calculator (frontend — zero API call) ────────────
const Cost = {
  calculate(pricePerTicket, ticketCount) {
    const base = parseFloat(pricePerTicket) * parseInt(ticketCount);
    const convenience = Math.round(base * 0.02);  // 2% convenience fee
    return { base, convenience, total: base + convenience };
  },
  display(pricePerTicket, ticketCount) {
    const { base, convenience, total } = this.calculate(pricePerTicket, ticketCount);
    return `Base: ${UI.rupee(base)} + Fee: ${UI.rupee(convenience)} = <strong>${UI.rupee(total)}</strong>`;
  }
};
