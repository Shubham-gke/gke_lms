// (function () {
//     function add_similar_courses_link() {
//         // Already added
//         if (document.getElementById("similar-courses-link")) {
//             return;
//         }

// 		console.log("jejjejj")

//         // Only logged-in users
//         if (frappe.session.user === "Guest") {
//             return;
//         }

//         const link = document.createElement("a");

//         link.id = "similar-courses-link";
//         link.href = "/similar-courses";
//         link.innerHTML = "Similar Courses →";

//         link.style.cssText = `
//             position: fixed;
//             top: 9px;
//             right: 20px;
//             z-index: 99999;
//             padding: 6px 14px;
//             border-radius: 6px;
//             border: 1px solid rgba(128,128,128,.4);
//             background: rgba(128,128,128,.18);
//             color: inherit;
//             font-size: 13px;
//             font-weight: 600;
//             text-decoration: none;
//             cursor: pointer;
//         `;

//         document.body.appendChild(link);
//     }

//     // Initial load
//     document.addEventListener("DOMContentLoaded", function () {
//         add_similar_courses_link();
//     });

//     // Frappe page/route change
//     if (window.frappe) {
//         $(document).on("app_ready", function () {
//             add_similar_courses_link();
//         });

//         $(document).on("page-change", function () {
//             setTimeout(add_similar_courses_link, 100);
//         });
//     }

//     // Extra safety for Vue SPA route changes
//     setInterval(function () {
//         add_similar_courses_link();
//     }, 1000);
// })();

console.log("🔥🔥🔥 LMS CUSTOM JS LOADED 🔥🔥🔥");

setTimeout(() => {
    console.log("🔥 Adding Similar Courses button");

    if (document.getElementById("similar-courses-btn")) {
        return;
    }

    const btn = document.createElement("button");

    btn.id = "similar-courses-btn";
    btn.innerHTML = "Suggested Courses →";

    btn.style.cssText = `
        position: fixed;
        top: 10px;
        right: 20px;
        z-index: 999999;
        padding: 8px 16px;
        border: 1px solid #ccc;
        border-radius: 6px;
        background: white;
        color: black;
        cursor: pointer;
        font-weight: 600;
    `;

    document.body.appendChild(btn);

    console.log("🔥 BUTTON ADDED");
}, 2000);