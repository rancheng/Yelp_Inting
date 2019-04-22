var chosen_list = [];

function record_ints(clicked_id) {
    var kw_btn = document.getElementById(clicked_id);

    var thenum = clicked_id.replace(/^\D+/g, '');
    var ind = chosen_list.indexOf(thenum);
    if (ind > -1) {
        kw_btn.style.backgroundColor = "transparent";
        chosen_list.splice(ind, 1);
    } else {
        kw_btn.style.backgroundColor = "#ff7496";
        chosen_list.push(thenum);
    }

}

function send_id_back() {
    $.ajax({
        type: "POST",
        contentType: "application/json;charset=utf-8",
        url: "/chosen_list",
        traditional: "true",
        data: JSON.stringify({chosen_list}),
        dataType: "json",
        success: function () {
            window.location.href = "/recommend_page";
        }
    });
}

// function send_id_back() {
//
// }