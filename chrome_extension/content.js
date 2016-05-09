// Pulls the data stored on /thoppe/arXiv2git/


function build_linkblock(name, A) {
    var base_url = "https://github.com/";

    if(!A.length) {
        return 0;
    }

    header_text = name + " (" + A.length + "): ";
    header = $("<h1>").append(header_text);

    X = $("<div>").addClass("arxiv2git");
    X.append(header);
        
    $.each(A, function(idx,val) {
        item = $("<a>").html(val).attr("href",base_url+val)
        X.append(item);

        if(idx+1 != A.length) {
            X.append(", ");
        }
        
    }); 

    $("body").append(X);

    return A.length;
};

function build_footer(n) {
    footer = $("<div>").addClass("arxiv2git");
    footer.append('<h1><a href="https://github.com/thoppe/arXiv2git">arXiv2git</a></h1> extension by <h1><a href="http://thoppe.github.io/">Travis Hoppe</a></h1>');

    if(n==0) {
        footer.append(" [No github links found] "); 
    }

    $("body").append(footer);
    console.log(n);
}

function load_a2g_data(url) {

    var total_items = 0;   

    $.getJSON(url, function(json) {
        var n = 0;
        n+=build_linkblock("github projects", json.project);
        n+=build_linkblock("github citations", json.citation);
        build_footer(n);
    }).fail(function(){build_footer(0);});

    

}


try {
    var arxivid_link  = $(".arxivid").find("a").attr('href');
    var arxivid = arxivid_link.replace("/abs/","");

    
    var a2g_url = ("https://raw.githubusercontent.com"+
               "/thoppe/arXiv2git"+
               "/master/data/a2g-links/"
               + arxivid.replace('/','_'));
}
catch (err) {
    console.log("Not a valid url for arXiv2git.");
}



if (a2g_url) {
    load_a2g_data(a2g_url);

}









