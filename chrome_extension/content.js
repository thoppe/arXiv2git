// content.js

var arxivid_link  = $(".arxivid").find("a").attr('href');
var arxivid = arxivid_link.replace("/abs/","");


var a2g_url = ("https://raw.githubusercontent.com"+
               "/thoppe/arXiv2git"+
               "/master/data/a2g-links/"
               + arxivid.replace('/','_'));

var projects  = [];
var citations = [];

$.getJSON(a2g_url, function(json) {

    console.log(json);


    $.each(json.project, function(idx,val) {
        var u = val;
        projects.push(u);
    });

    $.each(json.citation, function(idx,val) {
        var u = val;
        citations.push(u);
    });


    console.log(projects);
    console.log(citations);

    //console.log(a2g_url);

    //Creating Elements
    //var btn = document.createElement("BUTTON")
    //var t = document.createTextNode("CLICK ME!!!");
    //btn.appendChild(t);

    //Appending to DOM
    //document.body.insertBefore(btn, document.body.childNodes[0]);

    base_url = "https://github.com/"

    
    header = $("<h1>").append("Citations (",
                              citations.length,
                              "): ");
    
    C = $("<div>").addClass("arxiv2git");
    C.append(header);
        
    $.each(citations, function(idx,val) {
        item = $("<a>").html(val).attr("href",base_url+val)
        C.append(item);
        C.append(" ");
    }); 
    $("body").prepend(C);
        
    header = $("<h1>").append("Projects: (",
                              projects.length,
                              "): ");

    P = $("<div>").addClass("arxiv2git");
    P.append(header);
        
    $.each(projects, function(idx,val) {
        item = $("<a>").html(val).attr("href",base_url+val)
        P.append(item);
        P.append(" ");
    }); 
    $("body").prepend(P);
    


});




