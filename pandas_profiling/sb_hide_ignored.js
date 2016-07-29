/*function sb_toggle_viz(){
	var ignore_vars = document.getElementsByClassName('row variablerow ignore')

	for(var i = 0; i < ignore_vars.length; i++)
		{
		ignore_vars[i].style.visibility="hidden";
		}
}
*/
//<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

function sb_hide(){
    ignore_vars = $('div.ignore');

    cur_status = ignore_vars[0].style['display'];

    if (cur_status == 'none') {
            ignore_vars.show()
    } else {
            ignore_vars.hide()
    };
};


<script>
    document.getElementById('warnButton').onclick = function() {
            sb_hide();
    };
</script>


// finds specific p.h4 with text == varname
function findVarDiv(varname){
    var_p = $("p.h4").filter(function(index) { return this.textContent.match(varname)});
    return var_p.parent()[0];
}

// then, use findVarDiv(id).scrollIntoView(); to jump to
function jumpToVar(div_id){
    div_id.scrollIntoView()
}

// hahah fuck all taht noise
function buildDropdown(){
    //var all_vars = $('div.variablerow').map(function(index, dom) {return dom.id});
	//all_vars = $(all_vars).filter(function(index, val) {return val.length != 0})
    var s = $('<select />');

    var div_add_to = $('div.highlight').filter(function(index) { return this.textContent.match('Variables')});

    function appender(index, val){
        $('<option />', {value: val, text: val.replace('varid_', ''}).appendTo(s);
        };

    //$(all_vars).each(appender)

    $('div.variablerow').each(
        function(idx, val)
        {
        if (val.style['display'] != 'none')
            {
            if (val.id.length != 0)
                {
                appender(idx, val.id)
                }
            }
        }
    )

    s.appendTo($(div_add_to))

	s.change(function (v) {$('#'+v.target.value).get(0).scrollIntoView()})
}

function rebuildDropdown(){
    s = $('select')
    s.empty()

    $('div.variablerow').each(
        function(idx, val)
        {
        if (val.style['display'] != 'none')
            {
            if (val.id.length != 0)
                {
                appender(idx, val.id)
                }
            }
        }
    )
}
