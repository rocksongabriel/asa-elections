let form = document.getElementById("vote-form");
let checkboxes = document.getElementsByClassName("input-checkbox");
let vote_buttons = document.getElementsByClassName("checkbox-btn");
let labels = document.getElementsByClassName("checkbox-label");
let clear_vote_btn = document.getElementById("clearVoteBtn");
let voted_labels = document.getElementsByClassName("voted-label");
let submit_btn = document.getElementById("submitBtn");
let spinner = document.getElementById("spinner");
let voted_icon = document.getElementById("votedIcon");
let down_vote_btn = document.getElementById("downVoteBtn");
let up_vote_btn = document.getElementById("upVoteBtn");


// Reload the page when a user tries to go back
function preventBack() {
    window.history.forward();
}
setTimeout("preventBack()", 0);
window.onunload = function() {null};

// Prevent submission if the voter hasn't voted for anyone
form.addEventListener("submit", (event) => {
    let all_checked = false;
    for (checkbox of checkboxes) {
        all_checked = checkbox.checked || all_checked;
    }
    if (all_checked === true) {

        // disable the submit button and show the spin
        submit_btn.classList.add("pointer-events-none");
        spinner.classList.add("inline");
        spinner.classList.remove("hidden");

        form.submit(); // submit the form if one checkbox has been checked
    } else {
        event.preventDefault(); // if the person hasn't voted for anyone, don't submit
        alert("You haven't voted for anyone");
    }
})

// When the page is loaded, set all the checkboxes to false, 
// This will ensure that even if a voter refreshes their page 
// they wouldn't have accidentally voted twice
window.addEventListener("load", () => {
    for (checkbox of checkboxes) {
        checkbox.checked = false;
    }
})

// Remove votes 
clear_vote_btn.addEventListener("click", () => {
    // hide the voted label
    for (checkbox of checkboxes) {
        if (checkbox.checked) {
            identifier_class = checkbox.classList[0]; // the classname to get the voted label to display
            for (voted_label of voted_labels) {
                if (voted_label.classList.contains(identifier_class)) {
                    voted_label.classList.add("hidden"); // hide the voted text
                }
            }
        }
    }

    // uncheck the checkboxes
    for (checkbox of checkboxes) {
        checkbox.checked = false;
    }

    // enable the vote buttons 
    for (button of vote_buttons) {
        button.classList.remove("pointer-events-none");
    }

    // remove the opacity on the labels
    for (label of labels) {
        label.classList.remove("opacity-50");
    }
})

// Check if the user has clicked on a vote button
// If he has, disable all the buttons
for (checkbox of checkboxes) {
    checkbox.addEventListener("change", () => {
        for (button of vote_buttons) {
            button.classList.add("pointer-events-none"); // disable the button 
        }
        for (label of labels) {
            label.classList.add("opacity-50");
        }

        for (checkbox of checkboxes) {
            if (checkbox.checked) {
                identifier_class = checkbox.classList[0]; // the classname to get the voted label to display
                for (voted_label of voted_labels) {
                    if (voted_label.classList.contains(identifier_class)) {
                        voted_label.classList.remove("hidden"); // show the voted text
                    }
                }
            }
        }
    })
}

// Downvote an individual 
down_vote_btn.addEventListener("click", () => {
    voted_icon.classList.remove(...["fa-caret-up", "text-green-600"])
    voted_icon.classList.add(...["fa-caret-down", "text-red-600"])
})

// Upvote an individual
up_vote_btn.addEventListener("click", () => {
    voted_icon.classList.remove(...["fa-caret-down", "text-red-600"])
    voted_icon.classList.add(...["fa-caret-up", "text-green-600"])
})