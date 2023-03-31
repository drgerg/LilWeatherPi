difference(){
    union(){


        color("green")
        translate([20,0,6])
        cube([80,36,6]);
        translate([(121/2-14),36,6])
        cube([28,80,6]);

        color("red")
        translate([20,-4,0])
        cube([80,4,12]);

        color("blue")
        translate([20,36,0])
        cube([80,4,12]);
        // color("teal")
        // translate([74,36,0])
        // cube([26,4,12]);
        }
$fn=64;
    union(){
        translate([(121/2-10),18,30])
        cylinder(h=60,d=4,center=true);
        translate([(121/2+10),18,30])
        cylinder(h=60,d=4,center=true);
        translate([121/2,75,30])
        cylinder(h=60,d=4,center=true);
        translate([121/2,95,30])
        cylinder(h=60,d=4,center=true);
        translate([4,0,0])
        cube([113,36,6]);
        translate([(121/2-14),36,0])
        cube([28,80,6]);
        translate([60,36,17])
        union(){
            // cube([21.3,19.25,12],center=true);
            cylinder(h=40,d=7.7,center=true);
            translate([0,0,-10])
            cylinder(h=2.1,d=18.1,center=true);
            }
        translate([121/2,85,6])
        cube([30,6,4],center=true);
    }
}
// $fn=64;
// translate([60,36,17])
// difference(){
// cube([21.3,19.25,12],center=true);
// #cylinder(h=40,d=7,center=true);
// }