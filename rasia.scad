
include <roundedcube.scad>

$fn=80;
difference(){
  roundedcube([80,80,40],radius=3,apply_to="zmax");
  translate([2,2,-2])roundedcube([80-4,80-4,40],radius=1);
  translate([40,41,29]) cylinder(d=60,h=20);
  translate([0,0,-2])cube([90,45,27]);
  translate([73,70,20]) rotate([0,90,0]) cylinder(d=12,h=10);
  translate([69,10,32]) cylinder(d=7,h=10);
  translate([11,10,32]) cylinder(d=7,h=10);
}
