function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerText = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("skill-search");
  if (searchInput) {
    const searchForm = searchInput.closest("form");
    if (searchForm) {
      searchForm.addEventListener("submit", (e) => e.preventDefault());
    }

    searchInput.addEventListener("input", (e) => {
      const term = e.target.value.toLowerCase();
      const cards = document.querySelectorAll(".listing-card");
      const noResults = document.getElementById("no-results");
      let foundAny = false;

      cards.forEach((card) => {
        const titleLink = card.querySelector("h2 a");
        const teacherLink = card.querySelector(".teacher-link");
        const description = card.querySelector("p:last-of-type");

        if (titleLink && titleLink.dataset.originalText === undefined) {
          titleLink.dataset.originalText = titleLink.textContent;
        }
        if (teacherLink && teacherLink.dataset.originalText === undefined) {
          teacherLink.dataset.originalText = teacherLink.textContent;
        }
        if (description && description.dataset.originalText === undefined) {
          description.dataset.originalText = description.textContent;
        }

        const text = card.innerText.toLowerCase();
        const isMatch = text.includes(term);
        card.style.display = isMatch ? "block" : "none";
        if (isMatch) foundAny = true;

        if (titleLink) {
          titleLink.innerHTML = term
            ? highlightText(titleLink.dataset.originalText, term)
            : titleLink.dataset.originalText;
        }
        if (teacherLink) {
          teacherLink.innerHTML = term
            ? highlightText(teacherLink.dataset.originalText, term)
            : teacherLink.dataset.originalText;
        }
        if (description) {
          description.innerHTML = term
            ? highlightText(description.dataset.originalText, term)
            : description.dataset.originalText;
        }
      });

      if (noResults) noResults.style.display = foundAny ? "none" : "block";
    });
  }

  document.addEventListener("submit", (event) => {
    const form = event.target;
    const statusInput = form.querySelector('input[name="status"]');

    if (statusInput && statusInput.value === "cancelled") {
      const confirmed = confirm(
        "Are you sure you want to cancel this booking? This action cannot be undone.",
      );

      if (!confirmed) {
        event.preventDefault();
        return;
      }
    }

    const actionInput = form.querySelector('input[name="action"]');

    if (actionInput && actionInput.value === "delete") {
      const confirmed = confirm(
        "Are you sure you want to delete this listing? This action cannot be undone.",
      );

      if (!confirmed) {
        event.preventDefault();
      }
    }
  });

  document.querySelectorAll(".listing-age").forEach((el) => {
    const date = el.dataset.date;
    if (!date) return;

    el.textContent = timeAgo(date);
  });

  const toggle = document.getElementById("dark-toggle");

  if (toggle) {
    toggle.addEventListener("click", () => {
      const isDark = document.documentElement.classList.toggle("dark-mode");

      showToast(isDark ? "Dark Mode Enabled" : "Light Mode Enabled");

      localStorage.setItem(
        "darkMode",
        document.documentElement.classList.contains("dark-mode"),
      );
    });
  }

  function sortElements(containerId, cardClass, sortBy) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const cards = Array.from(container.querySelectorAll(cardClass));
    cards.sort((a, b) => {
      if (sortBy.startsWith("date")) {
        const dateA = new Date(a.dataset.date);
        const dateB = new Date(b.dataset.date);
        return sortBy === "date-asc" ? dateA - dateB : dateB - dateA;
      } else if (sortBy.startsWith("price")) {
        const priceA = parseFloat(a.dataset.price);
        const priceB = parseFloat(b.dataset.price);
        return sortBy === "price-asc" ? priceA - priceB : priceB - priceA;
      }
      return 0;
    });

    cards.forEach((card) => container.appendChild(card));
  }

  function timeAgo(dateString) {
    const createdDate = new Date(dateString);
    const now = new Date();

    const diffMs = now - createdDate;
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffWeeks = Math.floor(diffDays / 7);

    if (diffMinutes < 1) {
      return "Posted just now";
    } else if (diffMinutes < 60) {
      return `Posted ${diffMinutes} minute${diffMinutes !== 1 ? "s" : ""} ago`;
    } else if (diffHours < 24) {
      return `Posted ${diffHours} hour${diffHours !== 1 ? "s" : ""} ago`;
    } else if (diffDays < 7) {
      return `Posted ${diffDays} day${diffDays !== 1 ? "s" : ""} ago`;
    } else {
      return `Posted ${diffWeeks} week${diffWeeks !== 1 ? "s" : ""} ago`;
    }
  }

  function highlightText(text, term) {
    if (!term) return text;
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    return text.replace(
      new RegExp(escaped, "gi"),
      (match) => `<mark>${match}</mark>`,
    );
  }

  const sortSelect = document.getElementById("sort-select");
  if (sortSelect) {
    sortSelect.addEventListener("change", (e) => {
      const sortBy = e.target.value;
      sortElements("student-bookings", ".booking-card", sortBy);
      sortElements("teacher-bookings", ".booking-card", sortBy);
    });
  }

  const listingSortSelect = document.getElementById("listing-sort-select");
  if (listingSortSelect) {
    listingSortSelect.addEventListener("change", (e) => {
      const sortBy = e.target.value;
      sortElements("listings-container", ".listing-card", sortBy);
    });
  }
});
