
$(".radioRole input[name='role']").each(function( index ) {
  console.log( $( this ). prop("checked") )
})

$("input[name='role']").change(function(){
    console.log(1)
});
