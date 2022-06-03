const params = new Proxy(new URLSearchParams(window.location.search), {
  get: (searchParams, prop) => searchParams.get(prop),
});

document.getElementById("form-login").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = new FormData(e.target);
  const value = Object.fromEntries(data.entries());
  const req = await fetch("/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(value)
  });
  const res = await req.json();
  if (res.status === "OK") {
    setTimeout(() => {
      window.location.href = params.next || "/";
    }, 500);
    return Toast.success("Sign-up successful");
  }
  Toast.error(res.msg);
});
