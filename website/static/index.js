function deleteUrl(urlId) {
  fetch("/delete-url", {
    method: "POST",
    body: JSON.stringify({ urlId: urlId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
