from maya import cmds, mel
delete_nodes = cmds.ls(type=['expression', 'blendWeighted', 'animCurve'])
try:
    cmds.delete(delete_nodes)
except:
    pass

# handWeapons
handWeapon_joints = cmds.ls('*handWeapon*', type='joint')

# primary
primary_joints = cmds.ls('*_jnt', type='joint')
for hw_j in handWeapon_joints:
    primary_joints.remove(hw_j)

# sub
sub_joints = cmds.ls('*_subjnt*', type='joint')

# all
all_joints = cmds.ls('*root_jnt*', type='joint', dag=1)

# len(all_joints)
# len(primary_joints)
# len(sub_joints)
# len(handWeapon_joints)

# primary_joints_set
primary_joints_set = 'primary_joints_set'
if not cmds.objExists(primary_joints_set):
    cmds.sets(em=1, n=primary_joints_set)

for p_j in primary_joints:
    cmds.sets(p_j, add=primary_joints_set)

# sub_joints_set
sub_joints_set = 'sub_joints_set'
if not cmds.objExists(sub_joints_set):
    cmds.sets(em=1, n=sub_joints_set)

for p_j in sub_joints:
    cmds.sets(p_j, add=sub_joints_set)

# handWeapon_joints_set
handWeapon_joints_set = 'handWeapon_joints_set'
if not cmds.objExists(handWeapon_joints_set):
    cmds.sets(em=1, n=handWeapon_joints_set)

for p_j in handWeapon_joints:
    cmds.sets(p_j, add=handWeapon_joints_set)

# expressions
# arm
exp_name = 'subjnt_exp'
cmds.expression(s="""
proc float linear(float $input_x, float $sigma_val)
{
	return 1 - (($sigma_val - clamp(0.0, $sigma_val, $input_x)) / $sigma_val);
}

proc float cubic(float $input_x, float $sigma_val)
{
	$input_x /= $sigma_val;
	return 1 - max(1 - ($input_x * $input_x * $input_x), 0);
}

proc float gaussian(float $input_x, float $sigma_val)
{
	return 1 - exp(-$input_x * ((1.0 / $sigma_val) * (1.0 / $sigma_val)));
}

/*
proc float gaussian(float $input_x, float $center_u, float $sigma_val)
{
	float $total_num = ($input_x - $center_u) * ($input_x - $center_u);
	if ($sigma_val == 0.0)
	{
	return 0.0;
	}
	else
	{
	return exp(-$total_num / (2 * $sigma_val * $sigma_val));
	}
}
*/


////////////////////////////////////////////////////////////
// Quaternion
proc float convert_to_degrees(float $radians){
    float $pi = 3.1415927;
    float $result = $radians*180 / $pi;
    return $result;
}

proc float convert_to_radians(float $degrees){
    float $pi = 3.1415927;
    float $result = $degrees/180 * $pi;
    return $result;
}

proc float[] toQuaternion(float $yaw_z, float $pitch_y, float $roll_x, int $order){
    // yaw (Z), pitch (Y), roll (X)
    $yaw = convert_to_radians($yaw_z);
    $pitch = convert_to_radians($pitch_y);
    $roll = convert_to_radians($roll_x);

    float $qx = 0;
    float $qy = 0;
    float $qz = 0;
    float $qw = 0;

    float $qurt[];

    if ($order == 0){
				$qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 1){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 2){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 3){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 4){
        $qx += sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
        $qy += sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qz += cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5) + sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }
    else if ($order == 5){
        $qx += cos($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5) + sin($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5);
        $qy += cos($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qz += sin($roll * 0.5) * sin($pitch * 0.5) * cos($yaw * 0.5) + cos($roll * 0.5) * cos($pitch * 0.5) * sin($yaw * 0.5);
        $qw += cos($roll * 0.5) * cos($pitch * 0.5) * cos($yaw * 0.5) - sin($roll * 0.5) * sin($pitch * 0.5) * sin($yaw * 0.5);
    }

    $qurt[0] = $qw;
    $qurt[1] = $qx;
    $qurt[2] = $qy;
    $qurt[3] = $qz;

    return $qurt;

}

proc float[] toEuler(float $quartw, float $quartx, float $quarty, float $quartz){
    float $euler[];

    // roll (x-axis rotation)
    float $sinr_cosp = 2 * ($quartw * $quartx + $quarty * $quartz);
    float $cosr_cosp = 1 - 2 * ($quartx * $quartx + $quarty * $quarty);

    $euler[0] = convert_to_degrees(atan2($sinr_cosp, $cosr_cosp));

    // pitch (y-axis rotation)
    float $sinp = 2 * ($quartw * $quarty - $quartz * $quartx);
    float $pi = 3.1415927;
    if (abs($sinp) >= 1){
        $euler[1] = convert_to_degrees(-1 * $pi / 2);
    }
    else{
        $euler[1] = convert_to_degrees(asin($sinp));
    }

    // yaw (z-axis rotation)
    float $siny_cosp = 2 * ($quartw * $quartz + $quartx * $quarty);
    float $cosy_cosp = 1 - 2 * ($quarty * $quarty + $quartz * $quartz);
    $euler[2] = convert_to_degrees(atan2($siny_cosp, $cosy_cosp));

    return $euler;
}

proc float crop_rotation(float $angle){
    if ($angle > 180){
        return $angle -360;
    }
    else if ($angle < -180){
        return $angle + 360;
    }
    else{
        return $angle;
    }
}

proc float[] quaternion_multiply(float $q0w, float $q0x, float $q0y, float $q0z, float $q1w, float $q1x, float $q1y, float $q1z){
	float $mm0 = -$q1x * $q0x - $q1y * $q0y - $q1z * $q0z + $q1w * $q0w;
	float $mm1 = $q1x * $q0w + $q1y * $q0z - $q1z * $q0y + $q1w * $q0x;
	float $mm2 = -$q1x * $q0z + $q1y * $q0w + $q1z * $q0x + $q1w * $q0y;
	float $mm3 = $q1x * $q0y - $q1y * $q0x + $q1z * $q0w + $q1w * $q0z;

	float $mm[];
	$mm[0] = $mm0;
	$mm[1] = $mm1;
	$mm[2] = $mm2;
	$mm[3] = $mm3;

	return $mm;

}

proc float dot_quaternion(float $q0w, float $q0x, float $q0y, float $q0z, float $q1w, float $q1x, float $q1y, float $q1z){
	float $dotValue = ($q0w * $q1w) + ($q0x * $q1x) + ($q0y * $q1y) + ($q0z * $q1z);
	if ($dotValue < -1.0){
		$dotValue = -1.0;
	}
	else if ($dotValue > 1.0){
		$dotValue = 1.0;
	}
	return $dotValue;
}


proc float[] quaternion_to_angle(float $qw, float $qx, float $qy, float $qz){
	float $angle_results[];
	float $angle = 2 * acos($qw);
	$angle_results[0] = convert_to_degrees($angle);

	float $s = sqrt(1-$qw*$qw);
	if ($s < 0.00000001) {
		$angle_results[1] = $qx;
		$angle_results[2] = $qy;
		$angle_results[3] = $qz;
	}
	else
	{
		$angle_results[1] = $qx / $s;
		$angle_results[2] = $qy / $s;
		$angle_results[3] = $qz / $s;
	}
	return $angle_results;
}


proc float[] angle_to_quaternion(float $angle, float $qx, float $qy, float $qz){
	float $s = sin($angle/2);
	float $q[];
	$q[0] = cos($angle/2);
	$q[1] = $qx * $s;
	$q[2] = $qy * $s;
	$q[3] = $qz * $s;
	return $q;
}


proc float[] quaternion_slerp(float $q0w, float $q0x, float $q0y, float $q0z, float $q1w, float $q1x, float $q1y, float $q1z, float $lambda){
	float $dotproduct = dot_quaternion($q0w, $q0x, $q0y, $q0z, $q1w, $q1x, $q1y, $q1z);

	$lambda=$lambda/2.0;

	float $theta = acos($dotproduct);
	if ($theta<0.0){
		$theta=-$theta;
	}

	float $st = sin($theta);
	float $sut = sin($lambda*$theta);
	float $sout = sin((1-$lambda)*$theta);
	float $coeff1 = $sout/$st;
	float $coeff2 = $sut/$st;

	float $qr[];

	$qr[0] = $coeff1*$q0w + $coeff2*$q1w;
	$qr[1] = $coeff1*$q0x + $coeff2*$q1x;
	$qr[2] = $coeff1*$q0y + $coeff2*$q1y;
	$qr[3] = $coeff1*$q0z + $coeff2*$q1z;

	return $qr;
}


proc float[] angleRot_from_rotToQuat(float $rx, float $ry, float $rz, float $order, float $slerp){
    float $quartd_A[] = toQuaternion($rz, $ry, $rx, 0);
    float $quat_slerp[] = quaternion_slerp(0,0,0,0,$quartd_A[0], $quartd_A[1], $quartd_A[2], $quartd_A[3], $slerp);
    float $quat_angle[] = quaternion_to_angle($quat_slerp[0], $quat_slerp[1], $quat_slerp[2], $quat_slerp[3]);
    return $quat_angle;
}

// head and neck
float $quat_angle[] = angleRot_from_rotToQuat(head_jnt.rotateX, head_jnt.rotateY, head_jnt.rotateZ, 0, 2);

neck_jnt_twist.rotateX = $quat_angle[3]*0.2*$quat_angle[0];

// shoulder
float $quat_angle[] = angleRot_from_rotToQuat(shoulderL_jnt.rotateX, shoulderL_jnt.rotateY, shoulderL_jnt.rotateZ, 0, 2);

armpitL_subjnt1.translateZ = clamp(10.341, 20, linear($quat_angle[0], 90) * $quat_angle[2] * -10 + 10.341);
armpitL_subjnt2.translateZ = clamp(-17, -10.081, linear($quat_angle[0], 90) * $quat_angle[2] * -20 + -10.081);
armpitL_subjnt2.translateX = clamp(5.541, 7, linear($quat_angle[0], 90) * $quat_angle[2] * 5 + 5.541);
armpitL_subjnt3.translateX = clamp(5.776, 20, linear($quat_angle[0], 90) * $quat_angle[3] * 20 + 5.776);

// arm
float $quat_angle[] = angleRot_from_rotToQuat(armL_jnt.rotateX, armL_jnt.rotateY, armL_jnt.rotateZ, 0, 2);

armL_subjnt_bend_rot.rotateX = $quat_angle[1]*armL_jnt.xMult*$quat_angle[0];
armL_subjnt_bend_rot.rotateY = $quat_angle[2]*armL_jnt.yMult*$quat_angle[0];
armL_subjnt_bend_rot.rotateZ = $quat_angle[3]*armL_jnt.zMult*$quat_angle[0];

armL_subjnt_twist_rot.rotateX = $quat_angle[1]*-0.5*$quat_angle[0];

armL_subjnt1.translateX = clamp(0, 20, linear($quat_angle[0], 90) * $quat_angle[2] * -5);
armL_subjnt1.translateZ = clamp(7, 20, linear($quat_angle[0], 90) * $quat_angle[2] * -10 + 7);

armL_subjnt2.translateZ = clamp(-20, -7, linear($quat_angle[0], 120) * $quat_angle[2] * -20 + -7);
armL_subjnt3.translateY = clamp(6.2, 20, linear($quat_angle[0], 90) * $quat_angle[3] * 10 + 10);

armR_subjnt.rotateX = armR_jnt.rotateX*-0.5;

// elbow
float $quat_angle[] = angleRot_from_rotToQuat(forearmL_jnt.rotateX, forearmL_jnt.rotateY, forearmL_jnt.rotateZ, 0, 2);

elbowL_subjnt.translateX = clamp(-10, 0, linear($quat_angle[0], 90) * $quat_angle[2] * 3);
elbowL_subjnt.translateZ = clamp(-10, -2, linear($quat_angle[0], 90) * $quat_angle[2] * 3 + -2);

elbowL_subjnt1.translateX = clamp(0, 10, linear($quat_angle[0], 90) * $quat_angle[2] * -3);
elbowL_subjnt1.translateZ = clamp(2, 10, linear($quat_angle[0], 90) * $quat_angle[2] * -3 + 2);

forearmL_subjnt_twist_pos.translateZ = clamp(6, 20, linear($quat_angle[0], 90) * $quat_angle[2] * -3 + 6);

// hand
float $quat_angle[] = angleRot_from_rotToQuat(handL_jnt.rotateX, handL_jnt.rotateY, handL_jnt.rotateZ, 0, 2);

handL_subjnt.rotateX = $quat_angle[1]*0.7*$quat_angle[0];
handL_subjnt.rotateY = $quat_angle[2]*0*$quat_angle[0];
handL_subjnt.rotateZ = $quat_angle[3]*0*$quat_angle[0];

forearmL_subjnt_twist.rotateX = $quat_angle[1]*0.5*$quat_angle[0];

// upleg
float $quat_angle[] = angleRot_from_rotToQuat(uplegL_jnt.rotateX, uplegL_jnt.rotateY, uplegL_jnt.rotateZ, 0, 2);

uplegL_subjnt_bend.rotateX = $quat_angle[1]*uplegL_jnt.xMult*$quat_angle[0];
uplegL_subjnt_bend.rotateY = $quat_angle[2]*uplegL_jnt.yMult*$quat_angle[0];
uplegL_subjnt_bend.rotateZ = $quat_angle[3]*uplegL_jnt.zMult*$quat_angle[0];

uplegL_subjnt_twist.rotateX = $quat_angle[1]*-0.5*$quat_angle[0];

uplegL_subjnt_4.translateZ = clamp(7, 20, linear($quat_angle[0], 90) * $quat_angle[2] * -10 + 7);
uplegL_subjnt_3.translateZ = clamp(-20, -7, linear($quat_angle[0], 90) * $quat_angle[2] * -10 + -7);

// knee
float $quat_angle[] = angleRot_from_rotToQuat(legL_jnt.rotateX, legL_jnt.rotateY, legL_jnt.rotateZ, 0, 2);

kneeL_subjnt.translateX = clamp(-10, 0, linear($quat_angle[0], 90) * $quat_angle[2] * 3);
kneeL_subjnt.translateZ = clamp(-10, -2, linear($quat_angle[0], 90) * $quat_angle[2] * 3 + -2);

kneeL_subjnt_pos.translateZ = clamp(9, 20, linear($quat_angle[0], 90) * $quat_angle[2] * -7 + 9);

// foot
float $quat_angle[] = angleRot_from_rotToQuat(footL_jnt.rotateX, footL_jnt.rotateY, footL_jnt.rotateZ, 0, 2);

kneeL_subjnt_twist.rotateX = $quat_angle[1]*0.5*$quat_angle[0];

""", n='{0}'.format(exp_name), ae=0)
