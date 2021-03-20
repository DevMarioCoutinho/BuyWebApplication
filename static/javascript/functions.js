
function FormatCode(e) {
    var chr = String.fromCharCode(e.which);
    str = "1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM" 
    
    
    if (str.indexOf(chr) < 0)
      return false;

};

function FormatDescription(e) {
  var chr = String.fromCharCode(e.which);
  str = "1234567890qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM " 
  
  
  if (str.indexOf(chr) < 0)
    return false;


};

function FormatNumeric(e) {
  var chr = String.fromCharCode(e.which);
  str = "1234567890" 
  
  
  if (str.indexOf(chr) < 0)
    return false;


};

function FormatName(e) {
  var chr = String.fromCharCode(e.which);
  str = "qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM " 
  
  
  if (str.indexOf(chr) < 0)
    return false;


};