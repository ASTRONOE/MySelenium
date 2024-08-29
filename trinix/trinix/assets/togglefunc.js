window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.my_clientside_library = {
    togglefunc:function(n_clicks){
        if(n_clicks === null || n_clicks === undefined){
            return dash_clientside.no_update;
        }
        tog_id = document.getElementById('tog');
        con = document.getElementsByTagName("main")[0];
        tog_id.innerHTML = "Toggle";
        con.classList.toggle('dark-mode');
        document.body.classList.toggle('dark-mode');
        //content.classList.toggle('dark-mode');
        //toggle.classList.toggle('dark-mode');
        },

    }


    