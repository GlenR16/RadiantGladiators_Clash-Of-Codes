function likeAccept(toUser) {
  let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']");
  let formData = new FormData();
  formData.append("csrfmiddlewaretoken", csrfToken.value);
  formData.append("id", toUser);
  formData.append("swipe", "swipeRight");
  fetch("/api/", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data.submitted) return alert("Some Error occured!");
    })
    .catch((err) => console.log(err));
}
function dislikeReject(toUser) {
  let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']");
  let formData = new FormData();
  formData.append("csrfmiddlewaretoken", csrfToken.value);
  formData.append("id", toUser);
  formData.append("swipe", "LEFT");
  fetch("/api/", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data.submitted) return alert("Some Error occured!");
    })
    .catch((err) => console.log(err));
}
