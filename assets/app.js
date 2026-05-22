document.addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;

  const deleteButton = event.target.closest("[data-delete-url]");
  if (deleteButton) {
    event.preventDefault();
    await deleteImage(deleteButton);
    return;
  }

  const loadLink = event.target.closest("#load-more a");
  if (loadLink) {
    event.preventDefault();
    await loadMore(loadLink.closest("#load-more"));
  }
});

async function deleteImage(button) {
  const card = button.closest(".image-card");
  button.disabled = true;

  const response = await fetch(button.dataset.deleteUrl, { method: "DELETE" });
  if (response.ok) {
    card?.remove();
    return;
  }

  button.disabled = false;
}

const grid = document.querySelector("#image-grid");
const observer = "IntersectionObserver" in window
  ? new IntersectionObserver(onIntersect, { rootMargin: "600px" })
  : null;

function observeLoadMore() {
  if (!observer) return;

  observer.disconnect();
  const loadMore = document.querySelector("#load-more[data-load-url]");
  if (loadMore) observer.observe(loadMore);
}

async function onIntersect(entries) {
  const entry = entries.find((item) => item.isIntersecting);
  if (entry) await loadMore(entry.target);
}

async function loadMore(loadMoreElement) {
  if (!grid || !loadMoreElement?.dataset.loadUrl || loadMoreElement.dataset.loading === "true") {
    return;
  }

  loadMoreElement.dataset.loading = "true";
  const response = await fetch(loadMoreElement.dataset.loadUrl, {
    headers: { Accept: "text/html" },
  });
  if (!response.ok) {
    delete loadMoreElement.dataset.loading;
    return;
  }

  const doc = new DOMParser().parseFromString(await response.text(), "text/html");
  grid.append(...doc.querySelectorAll(".image-card"));

  const nextLoadMore = doc.querySelector("#load-more");
  loadMoreElement.replaceWith(nextLoadMore || document.createElement("div"));
  observeLoadMore();
}

observeLoadMore();
