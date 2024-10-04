document.addEventListener("DOMContentLoaded", () => {
    /* Tooltip */
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));

    /* Link */
    document.querySelectorAll("a:not([href^='#'])").forEach(el => el.setAttribute("target", "_blank"));

    /* Variables Dropdown */
    const variablesDropdown = document.querySelector("select#variables-dropdown");
    variablesDropdown.addEventListener("change", () => {
        const searchText = variablesDropdown.value.toLowerCase();

        document.querySelectorAll(".variable").forEach(el => {
            const title = el.firstElementChild.firstElementChild.firstElementChild.getAttribute("title").toLowerCase();
            let isMatch = title === (searchText);

            if (searchText === "") {
                isMatch = true
            }

            if (isMatch) {
                el.parentElement.classList.remove("d-none");
            } else {
                el.parentElement.classList.add("d-none");
            }
        });
    });

    /* Correlation */
    document.querySelector("#toggle-correlation-description")?.click(() => {
        document.querySelectorAll(".correlation-description").forEach(el => el.classList.toggle("d-none"));

        document.querySelectorAll(".tab-pane[id^=correlations_tab-]").forEach(el => {
            const diagramLength = el.querySelectorAll(".tab-pane[id^=correlations_tab-]").length;

            let classes = [];
            if (diagramLength === 1) {
                classes = ["col-sm-6", "col-sm-12"];
            } else if (diagramLength === 2) {
                classes = ["col-sm-4", "col-sm-6"];
            } else if (diagramLength === 3) {
                classes = ["col-sm-3", "col-sm-4"];
            } else {
                console.log("unsupported number of reports");
            }

            document.querySelectorAll(".correlation-diagram").forEach(el => {
                classes.forEach(clz => el.classList.toggle(clz));
            });
        });
    });
});
