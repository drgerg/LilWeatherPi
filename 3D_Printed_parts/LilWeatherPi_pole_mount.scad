difference(){
    union(){
        translate([4,0,42])
        cube([113,36,6]);
        cube([4,36,55]);
        translate([117,0,0])
        cube([4,36,55]);
        translate([(121/2-14),36,42])
        cube([28,80,6]);
        }
translate([-2,4,48])
cube([126,28,3]);

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
    }
}