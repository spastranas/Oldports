

//   for adding a picture I used the class example, java example #63 add a picture.

    // begin of update text
    var defaultURL = "/carrusel";
        d3.json(defaultURL,function(GetPicDetails) {
            // console.log(GetPicDetails);
                     FileAddress=GetPicDetails[0]["FileAddress"];
                     landmark=GetPicDetails[0]["landmark"];
                     state=GetPicDetails[0]["state"];
                     city=GetPicDetails[0]["city"];
                     index=GetPicDetails[0]["index"];                                            
        
         console.log("test created variables:")
         console.log(FileAddress);

         
                            
            d3.select("#img-gallery").selectAll("div")
            .data(GetPicDetails)
            .enter() // creates placeholder for new data
             .append("div") // appends a div to placeholder
             .classed("column", true) // sets the class of the new div
            .html(function(d) {
                return `<img src="${d.FileAddress}" >`;
                // return `<img class="rotate" src="${d.FileAddress}" height="600" width="400">`;
            }); // sets the html in the div to an image tag with the link
            


    })   ;
   


{/* <img class="rotate" src="/images/NFNOscarsDonut.jpg" height="400" width="600"/> */}


       