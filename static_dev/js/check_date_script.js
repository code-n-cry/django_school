var xmlHttp;
function srvTime(){
    try {
        xmlHttp = new XMLHttpRequest();
    }
    catch (err1) {
        try {
            xmlHttp = new ActiveXObject('Msxml2.XMLHTTP');
        }
        catch (err2) {
            try {
                xmlHttp = new ActiveXObject('Microsoft.XMLHTTP');
            }
            catch (eerr3) {
                console.error("AJAX not supported");
            }
        }
    }
    xmlHttp.open('HEAD',window.location.href.toString(),false);
    xmlHttp.setRequestHeader("Content-Type", "text/html");
    xmlHttp.send('');
    return xmlHttp.getResponseHeader("Date");
}
var server_time = new Date(srvTime());
var client_time = new Date()
var time_difference = (client_time - server_time) / 1000 / 3600
if (-24 < time_difference < 24) {
    document.getElementById('footer_date').textContent = `© ${client_time.getFullYear()} Schukin Egor`
}
