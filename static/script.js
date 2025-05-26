// FORM SUBMISSION & JSON DOWNLOAD
document.getElementById("upload-form").addEventListener("submit", async function(e) {
    e.preventDefault();
  
    const fileInput = document.getElementById("file");
    const outcomesText = document.getElementById("learning-outcomes").value;
    const loading = document.getElementById("loading");
    const errorDiv = document.getElementById("error");
  
    // Hide any existing errors
    errorDiv.style.display = "none";
  
    // Check if a file was selected
    if (fileInput.files.length === 0) {
      errorDiv.style.display = "block";
      errorDiv.textContent = "Please select a PDF or Word file.";
      return;
    }
  
    // Prepare form data
    const file = fileInput.files[0];
    const outcomes = outcomesText.split("\n").filter(line => line.trim() !== "");
    const formData = new FormData();
    formData.append("file", file);
    outcomes.forEach(outcome => formData.append("learning_outcomes", outcome));
  
    // Show loading spinner
    loading.style.display = "block";
  
    try {
      // POST request to FastAPI endpoint
      const response = await fetch("/generate_seed/", {
        method: "POST",
        body: formData
      });
  
      if (!response.ok) {
        throw new Error("Server returned an error");
      }
  
      // The response is a downloadable JSON file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "generated_articles.json"; // Match the filename set in main.py
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
  
      // CONFETTI BURST for success
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
  
      // Update stats counters with animation
      incrementCounter("docCount");
      incrementCounter("scriptCount");
  
    } catch (error) {
      // Show error message
      errorDiv.style.display = "block";
      errorDiv.textContent = "An error occurred: " + error.message;
    } finally {
      // Hide loading spinner
      loading.style.display = "none";
    }
  });
  
  // Function to increment a counter with a smooth animation using CountUp
  function incrementCounter(id) {
    const el = document.getElementById(id);
    const oldValue = parseInt(el.textContent, 10) || 0;
    const newValue = oldValue + 1;
    const countUpInstance = new countUp.CountUp(el, newValue, { duration: 1, separator: "," });
    countUpInstance.start();
  }
  
  // SCROLL-TO-TOP BUTTON
  const scrollTopBtn = document.getElementById("scrollTopBtn");
  
  // Show or hide button on scroll
  window.onscroll = function() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
      scrollTopBtn.style.display = "flex";
    } else {
      scrollTopBtn.style.display = "none";
    }
  };
  
  // When clicked, scroll to top smoothly
  scrollTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
  
  // DARK MODE TOGGLE
  const darkModeToggle = document.getElementById("darkModeToggle");
  darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    darkModeToggle.innerHTML = document.body.classList.contains("dark-mode")
      ? '<i class="bi bi-brightness-high me-1"></i>Light Mode'
      : '<i class="bi bi-moon-fill me-1"></i>Dark Mode';
  });
  
  // COUNTUP ANIMATIONS (initial load)
  window.addEventListener("load", () => {
    const counters = document.querySelectorAll(".count");
    counters.forEach((counter) => {
      const endVal = parseInt(counter.getAttribute("data-count"), 10);
      const countUpInstance = new countUp.CountUp(counter, endVal, { duration: 3, separator: "," });
      setTimeout(() => {
        if (!countUpInstance.error) {
          countUpInstance.start();
        }
      }, 1000);
    });
  });
  
