function Animate() {

    $("#btn").click(function () {
        $("#CityList").slideToggle();

    });
    // $("#CityList").hover(function () {
    //     // $(this).slideDown();
    // }, function () {
    //     // $("#CityList").slideUp();
    //
    // });
    $("#navdiv").click(function () {
        $("#navdiv ul li").slideToggle("slow");

    });
    $("#btn ul").hover(function () {
        // alert("in");
    },function () {
                $(this).slideUp("slow");

    });
    // $("img").click(() => {
    //     Startanimate();
    // })
    //
    // $("img").hover(function () {
    //     $(this).animate({width:"+=200px", height: "500px"}, 2000);
    // }, function () {
    //     $(this).animate({width: "-=200px", height: "500px"}, 1000);
    //
    // });

}

function Startanimate() {
    var img = $("img").nextAll();

    img.toggle("slow");
    img.hover(function () {
            $(this).animate({width: "500px", height: "500px", right: "500px"}, "slow");
        },
        function () {
            // $(this).JingQucss({"width": "300px", "border-radius": "50%"});
            $(this).animate({width: "200px", height: "200px"}, "slow");

        }
    )


}
