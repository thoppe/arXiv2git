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
        return false;
    }

    header = $("<h1>").append(name, " (",A.length,"): ");

    X = $("<div>").addClass("arxiv2git");
    X.append(header);
        
    $.each(A, function(idx,val) {
        item = $("<a>").html(val).attr("href",base_url+val)
        X.append(item);
        X.append(", ");
    }); 
    $("body").prepend(X);

};


$.getJSON(a2g_url, function(json) {

    console.log(json);
    
    

    build_linkblock("Projects", json.project);
    build_linkblock("Citations", json.citation);

});




