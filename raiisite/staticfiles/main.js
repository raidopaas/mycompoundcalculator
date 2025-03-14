document.addEventListener("DOMContentLoaded", function() {
    const yearButtons = document.querySelectorAll(".toggle-year");
    const monthButtons = document.querySelectorAll(".toggle-month");

    // Toggle months when a year is clicked
    yearButtons.forEach(button => {
        button.addEventListener("click", function() {
            const yearKey = this.getAttribute("data-year");
            const monthRows = document.querySelectorAll(`.month-row[data-year='${yearKey}']`);
            const isExpanding = this.textContent === "+";

            monthRows.forEach(row => {
                row.style.display = isExpanding ? "table-row" : "none";
            });

            // If collapsing the year, also collapse its months and days
            if (!isExpanding) {
                const dayRows = document.querySelectorAll(`.day-row[data-month^='${yearKey}-']`);
                dayRows.forEach(row => row.style.display = "none");

                // Reset month expand buttons to "+"
                document.querySelectorAll(`.toggle-month[data-month^='${yearKey}-']`).forEach(btn => {
                    btn.textContent = "+";
                });
            }

            // Change year button text to "+" or "-"
            this.textContent = isExpanding ? "-" : "+";
        });
    });

    // Toggle days when a month is clicked
    monthButtons.forEach(button => {
        button.addEventListener("click", function() {
            const monthKey = this.getAttribute("data-month");
            const dayRows = document.querySelectorAll(`.day-row[data-month='${monthKey}']`);
            const isExpanding = this.textContent === "+";

            dayRows.forEach(row => {
                row.style.display = isExpanding ? "table-row" : "none";
            });

            // Change month button text to "+" or "-"
            this.textContent = isExpanding ? "-" : "+";
        });
    });
});
