var infobox = require('wiki-infobox');

var page = 'Narendra Modi';
var language = 'en';
 
infobox(page, language, function(err, data){
  if (err) {
    console.log(err); 
    return;
  }
 
  console.log(data);
  
});