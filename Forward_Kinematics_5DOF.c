#include <stdio.h>
#include <math.h>

#define pi 3.14159
void main()
{
  /*
  ASSUMPTION:

  BASE ANGLE=0.0
  SHOULDER ANGLE=90.0
  ELBOW ANGLE=0.0
  WRIST ANGLE=0.0
  GRIPPER ANGLE=90.0
  */
  float d_i[5]={1.0,0.0,0.0,0.0,1.0};      //distance traveled along z_i to bring it to origin
  float a_i[5]={0.0,0.0,1.0,1.0,0.0};         //Distance traveled along x_i to bring it to origin
  float alpha_i[5]={0.0,90.0,0.0,0.0,90.0};  //angle of rotation of x_i to align it to z_i-1 and z_i
  float theta[5]={0.0,0.0,0.0,0.0,0.0};    //ENTER VALUE OF THETA
  float Ex=sin(theta[0]+theta[1])*d_i[4]+cos(theta[0]+theta[1])*a_i[3]*cos(theta[2]+theta[3])+cos(theta[0]+theta[1])*a_i[2]*cos(theta[2]);
  float Ey=-cos(theta[0]+theta[1])*d_i[4]+sin(theta[0]+theta[1])*a_i[3]*cos(theta[2]+theta[3])+sin(theta[0]+theta[1])*a_i[2]*cos(theta[2]);
  float Ez=a_i[3]*sin(theta[2]+theta[3])+a_i[2]*sin(theta[2])+d_i[0];

  printf("END EFFECTOR Ex: %f",Ex);
  printf("\nEND EFFECTOR Ey: %f",Ey);
  printf("\nEND EFFECTOR Ez: %f",Ez);
}
