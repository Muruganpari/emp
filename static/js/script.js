form = document.getElementById("updateForm");

function updateEmployee(id, name, designation, age, email) {
fetch("/employee/" + id, {
    method: "PATCH",
    body: JSON.stringify({
      name,
      designation,
      age,
      email
    }),
  }).then((response) => response.json());
  window.location.reload();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const designation = document.getElementById("designation").value;
  const id = document.getElementById("id").value;
  const age = document.getElementById("age").value;
  const email = document.getElementById("email").value;

  updateEmployee(id, name, designation, age, email);
});

async function deleteEmployee(id) {
  const res = await fetch("/employee/" + id, {
    method: "DELETE",
  }).then((response) => response.json());
  window.location.reload();
}
