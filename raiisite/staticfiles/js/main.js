<script>
alert("main.js is loaded!");
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".toggle-btn").forEach(button => {
        button.addEventListener("click", function() {
            const monthKey = this.getAttribute("data-month");
            console.log("Clicked button for monthKey:", monthKey); // Debugging

            const dayRows = document.querySelectorAll(`.day-row[data-month='${monthKey}']`);
            console.log("Found rows:", dayRows.length); // Debugging

            dayRows.forEach(row => {
                row.style.display = row.style.display === "none" ? "table-row" : "none";
            });

            this.textContent = this.textContent === "+" ? "-" : "+";
        });
    });
});



/*    document.addEventListener("DOMContentLoaded", function() {
        const buttons = document.querySelectorAll(".toggle-btn");

        buttons.forEach(button => {
            button.addEventListener("click", function() {
                const monthKey = this.getAttribute("data-month");
                const dayRows = document.querySelectorAll(`.day-row[data-month='${monthKey}']`);
                
                dayRows.forEach(row => {
                    row.style.display = row.style.display === "none" ? "table-row" : "none";
                });

                // Change button text to "+" or "-" based on visibility
                this.textContent = this.textContent === "+" ? "-" : "+";
            });
        });
    });*/
</script>