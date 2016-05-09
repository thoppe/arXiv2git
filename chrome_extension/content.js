// Pulls the data stored on /thoppe/arXiv2git/

var arxivid_link  = $(".arxivid").find("a").attr('href');
var arxivid = arxivid_link.replace("/abs/","");

var a2g_url = ("https://raw.githubusercontent.com"+
               "/thoppe/arXiv2git"+
               "/master/data/a2g-links/"
               + arxivid.replace('/','_'));

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

    //$("body").prepend(X);
    $("body").append(X);

    return A.length;
};


$.getJSON(a2g_url, function(json) {

    console.log(json);
    
    var total_items = 0;
    total_items += build_linkblock("github projects", json.project);
    total_items += build_linkblock("github citations", json.citation);

    if(total_items) {

    }
    
});




