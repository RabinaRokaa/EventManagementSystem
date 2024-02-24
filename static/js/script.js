console.log("script running...asassas")
console.log("hello")
// function toggleSidebar() {
//     var sidebar = document.getElementById('sidebar');
//     var menuBar = document.getElementById('menuBar');
//     if (sidebar.style.display === 'none') {
//         sidebar.style.display = 'block';
//         menuBar.style.display = 'none'; // Hide menu bar when sidebar is displayed
//     } else {
//         sidebar.style.display = 'none';
//         menuBar.style.display = 'block'; // Show menu bar when sidebar is hidden
//     }
// }


// // Function to open sidebar
// function openNav() {
//     document.getElementById("sidebar").style.width = "250px";
// }

// Function to close sidebar
function closeSidebar() {
    var sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.style.display = 'none';
    }
}


// Function to toggle sidebar
function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    if (sidebar) {
        if (sidebar.style.display === 'none') {
            sidebar.style.display = 'block';
        } else {
            sidebar.style.display = 'none';
        }
    }
}

function highlightLink(link) {
    // Remove 'active' class from all links
    var links = document.querySelectorAll('.sidebar-link');
    links.forEach(function(item) {
        item.classList.remove('active');
    });
    
    // Add 'active' class to the clicked link
    link.classList.add('active');
}



//for the sidewise view
function loadVenueList() {
    // Send an AJAX request to fetch the venue list content
    fetch('/venue_list')
        .then(response => response.text())
        .then(data => {
            // Insert the venue list content sideways into the page
            document.getElementById('venue-list-container').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function loadUserList() {
    // Send an AJAX request to fetch the venue list content
    fetch('/user_list')
        .then(response => response.text())
        .then(data => {
            // Insert the venue list content sideways into the page
            document.getElementById('user-list-container').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}
