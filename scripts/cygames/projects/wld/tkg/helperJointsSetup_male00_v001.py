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
exp_name = 'arm_subjnt_exp'
cmds.expression(s="""
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

proc float[] toQuaternion(float $yaw_z, float $pitch_y, float $roll_x){
    // yaw (Z), pitch (Y), roll (X)
    $yaw = convert_to_radians($yaw_z);
    $pitch = convert_to_radians($pitch_y);
    $roll = convert_to_radians($roll_x);

    float $cy = cos($yaw * 0.5);
    float $sy = sin($yaw * 0.5);
    float $cp = cos($pitch * 0.5);
    float $sp = sin($pitch * 0.5);
    float $cr = cos($roll * 0.5);
    float $sr = sin($roll * 0.5);

    float $qurt[];

    float $qw = $cy * $cp * $cr + $sy * $sp * $sr;
    float $qx = $cy * $cp * $sr - $sy * $sp * $cr;
    float $qy = $sy * $cp * $sr + $cy * $sp * $cr;
    float $qz = $sy * $cp * $cr - $cy * $sp * $sr;

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

    $euler[0] = atan2($sinr_cosp, $cosr_cosp);

    // pitch (y-axis rotation)
    float $sinp = 2 * ($quartw * $quarty - $quartz * $quartx);
    float $pi = 3.1415927;
    if (abs($sinp) >= 1){
        $euler[1] = -1 * $pi / 2;
    }
    else{
        $euler[1] = asin($sinp);
    }

    // yaw (z-axis rotation)
    float $siny_cosp = 2 * ($quartw * $quartz + $quartx * $quarty);
    float $cosy_cosp = 1 - 2 * ($quarty * $quarty + $quartz * $quartz);
    $euler[2] = atan2($siny_cosp, $cosy_cosp);

    return $euler;
}

proc float[] eulerToQuaternionToEuler(float $roll, float $pitch, float $yaw){
	float $e2q2e[];

	float $quartd[] = toQuaternion($yaw, $pitch, $roll);
	float $eulerd[] = toEuler($quartd[0], $quartd[1], $quartd[2], $quartd[3]);

	$e2q2e[0]=convert_to_degrees($eulerd[0]);
	$e2q2e[1]=convert_to_degrees($eulerd[1]);
	$e2q2e[2]=convert_to_degrees($eulerd[2]);

	return $e2q2e;

}

proc float relax_gimbal_rotation(float $pitchRot, float $srcRot, float $dstRot, float $ratio){
	// float $ratio = 90; // Pitch
	// float $pitchRot = uplegL_subjnt_3.rotateY;
	float $relax = 1 - abs($pitchRot) / $ratio;

	if ($srcRot > 90)
	{
		$dstRot = (180 - $srcRot) * $relax;
	}
	else if ($srcRot < -90)
	{
		$dstRot = -(180 + $srcRot) * $relax;
	}
	else
		$dstRot = $srcRot * $relax;

	return $dstRot;

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

// Left
float $eulerd_L[] = eulerToQuaternionToEuler(armL_jnt.rotateX, armL_jnt.rotateY, armL_jnt.rotateZ); // (Roll, Pitch, Yaw)
armL_subjnt.rotateX = relax_gimbal_rotation($eulerd_L[1], $eulerd_L[0], armL_subjnt.rotateX, 90) * -0.5;


// Right
float $eulerd_R[] = eulerToQuaternionToEuler(armR_jnt.rotateX, armR_jnt.rotateY, armR_jnt.rotateZ); // (Roll, Pitch, Yaw)
armR_subjnt.rotateX = relax_gimbal_rotation($eulerd_R[1], $eulerd_R[0], armR_subjnt.rotateX, 90) * -0.5;

""", n='{0}'.format(exp_name), ae=0)

exp_name = 'hand_subjnt_exp'
cmds.expression(s="""
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

proc float[] toQuaternion(float $yaw_z, float $pitch_y, float $roll_x){
    // yaw (Z), pitch (Y), roll (X)
    $yaw = convert_to_radians($yaw_z);
    $pitch = convert_to_radians($pitch_y);
    $roll = convert_to_radians($roll_x);

    float $cy = cos($yaw * 0.5);
    float $sy = sin($yaw * 0.5);
    float $cp = cos($pitch * 0.5);
    float $sp = sin($pitch * 0.5);
    float $cr = cos($roll * 0.5);
    float $sr = sin($roll * 0.5);

    float $qurt[];

    float $qw = $cy * $cp * $cr + $sy * $sp * $sr;
    float $qx = $cy * $cp * $sr - $sy * $sp * $cr;
    float $qy = $sy * $cp * $sr + $cy * $sp * $cr;
    float $qz = $sy * $cp * $cr - $cy * $sp * $sr;

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

    $euler[0] = atan2($sinr_cosp, $cosr_cosp);

    // pitch (y-axis rotation)
    float $sinp = 2 * ($quartw * $quarty - $quartz * $quartx);
    float $pi = 3.1415927;
    if (abs($sinp) >= 1){
        $euler[1] = -1 * $pi / 2;
    }
    else{
        $euler[1] = asin($sinp);
    }

    // yaw (z-axis rotation)
    float $siny_cosp = 2 * ($quartw * $quartz + $quartx * $quarty);
    float $cosy_cosp = 1 - 2 * ($quarty * $quarty + $quartz * $quartz);
    $euler[2] = atan2($siny_cosp, $cosy_cosp);

    return $euler;
}

proc float[] eulerToQuaternionToEuler(float $roll, float $pitch, float $yaw){
	float $e2q2e[];

	float $quartd[] = toQuaternion($yaw, $pitch, $roll);
	float $eulerd[] = toEuler($quartd[0], $quartd[1], $quartd[2], $quartd[3]);

	$e2q2e[0]=convert_to_degrees($eulerd[0]);
	$e2q2e[1]=convert_to_degrees($eulerd[1]);
	$e2q2e[2]=convert_to_degrees($eulerd[2]);

	return $e2q2e;

}

proc float relax_gimbal_rotation(float $pitchRot, float $srcRot, float $dstRot, float $ratio){
	// float $ratio = 90; // Pitch
	// float $pitchRot = uplegL_subjnt_3.rotateY;
	float $relax = 1 - abs($pitchRot) / $ratio;

	if ($srcRot > 90)
	{
		$dstRot = (180 - $srcRot) * $relax;
	}
	else if ($srcRot < -90)
	{
		$dstRot = -(180 + $srcRot) * $relax;
	}
	else
		$dstRot = $srcRot * $relax;

	return $dstRot;

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

// Left
float $eulerd_L[] = eulerToQuaternionToEuler(handL_jnt.rotateX, handL_jnt.rotateY, handL_jnt.rotateZ); // (Roll, Pitch, Yaw)
handL_subjnt.rotateX = relax_gimbal_rotation($eulerd_L[1], $eulerd_L[0], handL_subjnt.rotateX, 90) * 0.7;

// Right
float $eulerd_R[] = eulerToQuaternionToEuler(handR_jnt.rotateX, handR_jnt.rotateY, handR_jnt.rotateZ); // (Roll, Pitch, Yaw)
handR_subjnt.rotateX = relax_gimbal_rotation($eulerd_R[1], $eulerd_R[0], handR_subjnt.rotateX, 90) * 0.7;

 """, n='{0}'.format(exp_name), ae=0)

exp_name = 'upleg_subjnt_exp'
cmds.expression(s="""
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

proc float[] toQuaternion(float $yaw_z, float $pitch_y, float $roll_x){
    // yaw (Z), pitch (Y), roll (X)
    $yaw = convert_to_radians($yaw_z);
    $pitch = convert_to_radians($pitch_y);
    $roll = convert_to_radians($roll_x);

    float $cy = cos($yaw * 0.5);
    float $sy = sin($yaw * 0.5);
    float $cp = cos($pitch * 0.5);
    float $sp = sin($pitch * 0.5);
    float $cr = cos($roll * 0.5);
    float $sr = sin($roll * 0.5);

    float $qurt[];

    float $qw = $cy * $cp * $cr + $sy * $sp * $sr;
    float $qx = $cy * $cp * $sr - $sy * $sp * $cr;
    float $qy = $sy * $cp * $sr + $cy * $sp * $cr;
    float $qz = $sy * $cp * $cr - $cy * $sp * $sr;

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

    $euler[0] = atan2($sinr_cosp, $cosr_cosp);

    // pitch (y-axis rotation)
    float $sinp = 2 * ($quartw * $quarty - $quartz * $quartx);
    float $pi = 3.1415927;
    if (abs($sinp) >= 1){
        $euler[1] = -1 * $pi / 2;
    }
    else{
        $euler[1] = asin($sinp);
    }

    // yaw (z-axis rotation)
    float $siny_cosp = 2 * ($quartw * $quartz + $quartx * $quarty);
    float $cosy_cosp = 1 - 2 * ($quarty * $quarty + $quartz * $quartz);
    $euler[2] = atan2($siny_cosp, $cosy_cosp);

    return $euler;
}

proc float[] eulerToQuaternionToEuler(float $roll, float $pitch, float $yaw){
	float $e2q2e[];

	float $quartd[] = toQuaternion($yaw, $pitch, $roll);
	float $eulerd[] = toEuler($quartd[0], $quartd[1], $quartd[2], $quartd[3]);

	$e2q2e[0]=convert_to_degrees($eulerd[0]);
	$e2q2e[1]=convert_to_degrees($eulerd[1]);
	$e2q2e[2]=convert_to_degrees($eulerd[2]);

	return $e2q2e;

}

proc float relax_gimbal_rotation(float $pitchRot, float $srcRot, float $dstRot, float $ratio){
	// float $ratio = 90; // Pitch
	// float $pitchRot = uplegL_subjnt_3.rotateY;
	float $relax = 1 - abs($pitchRot) / $ratio;

	if ($srcRot > 90)
	{
		$dstRot = (180 - $srcRot) * $relax;
	}
	else if ($srcRot < -90)
	{
		$dstRot = -(180 + $srcRot) * $relax;
	}
	else
		$dstRot = $srcRot * $relax;

	return $dstRot;

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

// Left
float $eulerd_L[] = eulerToQuaternionToEuler(uplegL_jnt.rotateX, uplegL_jnt.rotateY, uplegL_jnt.rotateZ); // (Roll, Pitch, Yaw)
uplegL_subjnt_1.rotateX = relax_gimbal_rotation($eulerd_L[1], $eulerd_L[0], uplegL_subjnt_1.rotateX, 90) * -0.5;
uplegL_subjnt_2.rotateX = uplegL_subjnt_1.rotateX * 0.5;


// Right
float $eulerd_R[] = eulerToQuaternionToEuler(uplegR_jnt.rotateX, uplegR_jnt.rotateY, uplegR_jnt.rotateZ); // (Roll, Pitch, Yaw)
uplegR_subjnt_1.rotateX = relax_gimbal_rotation($eulerd_R[1], $eulerd_R[0], uplegR_subjnt_1.rotateX, 90) * -0.5;
uplegR_subjnt_2.rotateX = uplegR_subjnt_1.rotateX * 0.5;

""", n='{0}'.format(exp_name), ae=0)

exp_name = 'knee_subjnt_exp'
cmds.expression(s="""
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

proc float[] toQuaternion(float $yaw_z, float $pitch_y, float $roll_x){
    // yaw (Z), pitch (Y), roll (X)
    $yaw = convert_to_radians($yaw_z);
    $pitch = convert_to_radians($pitch_y);
    $roll = convert_to_radians($roll_x);

    float $cy = cos($yaw * 0.5);
    float $sy = sin($yaw * 0.5);
    float $cp = cos($pitch * 0.5);
    float $sp = sin($pitch * 0.5);
    float $cr = cos($roll * 0.5);
    float $sr = sin($roll * 0.5);

    float $qurt[];

    float $qw = $cy * $cp * $cr + $sy * $sp * $sr;
    float $qx = $cy * $cp * $sr - $sy * $sp * $cr;
    float $qy = $sy * $cp * $sr + $cy * $sp * $cr;
    float $qz = $sy * $cp * $cr - $cy * $sp * $sr;

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

    $euler[0] = atan2($sinr_cosp, $cosr_cosp);

    // pitch (y-axis rotation)
    float $sinp = 2 * ($quartw * $quarty - $quartz * $quartx);
    float $pi = 3.1415927;
    if (abs($sinp) >= 1){
        $euler[1] = -1 * $pi / 2;
    }
    else{
        $euler[1] = asin($sinp);
    }

    // yaw (z-axis rotation)
    float $siny_cosp = 2 * ($quartw * $quartz + $quartx * $quarty);
    float $cosy_cosp = 1 - 2 * ($quarty * $quarty + $quartz * $quartz);
    $euler[2] = atan2($siny_cosp, $cosy_cosp);

    return $euler;
}

proc float[] eulerToQuaternionToEuler(float $roll, float $pitch, float $yaw){
	float $e2q2e[];

	float $quartd[] = toQuaternion($yaw, $pitch, $roll);
	float $eulerd[] = toEuler($quartd[0], $quartd[1], $quartd[2], $quartd[3]);

	$e2q2e[0]=convert_to_degrees($eulerd[0]);
	$e2q2e[1]=convert_to_degrees($eulerd[1]);
	$e2q2e[2]=convert_to_degrees($eulerd[2]);

	return $e2q2e;

}

proc float relax_gimbal_rotation(float $pitchRot, float $srcRot, float $dstRot, float $ratio){
	// float $ratio = 90; // Pitch
	// float $pitchRot = uplegL_subjnt_3.rotateY;
	float $relax = 1 - abs($pitchRot) / $ratio;

	if ($srcRot > 90)
	{
		$dstRot = (180 - $srcRot) * $relax;
	}
	else if ($srcRot < -90)
	{
		$dstRot = -(180 + $srcRot) * $relax;
	}
	else
		$dstRot = $srcRot * $relax;

	return $dstRot;

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

// Left
float $eulerd_L[] = eulerToQuaternionToEuler(legL_jnt.rotateX, legL_jnt.rotateY, legL_jnt.rotateZ); // (Roll, Pitch, Yaw);
float $knee_L = $eulerd_L[1];
float $kneeL_tx_subvalue_A = 30.0;
float $kneeL_tz_subvalue_A = 90.0;
float $kneeL_ry_subvalue_A = -2.0;
kneeL_subjnt.translateX = $knee_L / $kneeL_tx_subvalue_A;
kneeL_subjnt.translateZ = $knee_L / $kneeL_tz_subvalue_A + -2;
kneeL_subjnt.rotateY = $knee_L / $kneeL_ry_subvalue_A;

float $kneeL_tx_subvalue_B = ($knee_L + 90.0)*-0.01667;
float $kneeL_tz_subvalue_B = ($knee_L + 90.0)*0.05;
float $kneeL_ry_subvalue_B = ($knee_L + 90.0)*-0.58334;
if ($knee_L < -90){
	kneeL_subjnt.translateX = -3 - $kneeL_tx_subvalue_B;
	kneeL_subjnt.translateZ = -3 - $kneeL_tz_subvalue_B;
	kneeL_subjnt.rotateY = 45 + $kneeL_ry_subvalue_B;

}

// Right
float $eulerd_R[] = eulerToQuaternionToEuler(legR_jnt.rotateX, legR_jnt.rotateY, legR_jnt.rotateZ); // (Roll, Pitch, Yaw);
float $knee_R = $eulerd_R[1];
float $kneeR_tx_subvalue_A = -30.0;
float $kneeR_tz_subvalue_A = -90.0;
float $kneeR_ry_subvalue_A = -2.0;
kneeR_subjnt.translateX = $knee_R / $kneeR_tx_subvalue_A;
kneeR_subjnt.translateZ = $knee_R / $kneeR_tz_subvalue_A + 2;
kneeR_subjnt.rotateY = $knee_R / $kneeR_ry_subvalue_A;

float $kneeR_tx_subvalue_B = ($knee_R + 90.0)*0.01667;
float $kneeR_tz_subvalue_B = ($knee_R + 90.0)*-0.05;
float $kneeR_ry_subvalue_B = ($knee_R + 90.0)*0.58334;
if (legR_jnt.rotateY < -90){
	kneeR_subjnt.translateX = 3 - $kneeR_tx_subvalue_B;
	kneeR_subjnt.translateZ = 3 - $kneeR_tz_subvalue_B;
	kneeR_subjnt.rotateY = 45 - $kneeR_ry_subvalue_B;

}
""", n='{0}'.format(exp_name), ae=0)


exp_name = 'armpit_subjnt_exp'
cmds.expression(s="""
// L init rotate
float $shoulderL_rz_init = 0.0;
float $armL_rz_init = -55.0;

// armpitL tx
float $shoulderL_armpitL_tx_subvalue_A = -0.1;
float $shoulderL_rz_armpitL_tx_result = (shoulderL_jnt.rotateZ - $shoulderL_rz_init) * $shoulderL_armpitL_tx_subvalue_A;

float $armL_armpitL_tx_subvalue_A = -0.1;
float $armL_rz_armpitL_tx_result = (armL_jnt.rotateZ - $armL_rz_init) * $armL_armpitL_tx_subvalue_A;

float $armpitL_tx_subvalue_init = 9.23725;
armpitL_subjnt.translateX = clamp(0, 12, ($shoulderL_rz_armpitL_tx_result + $armL_rz_armpitL_tx_result) / 2 + $armpitL_tx_subvalue_init);

// armpitL ty
float $shoulderL_armpitL_ty_subvalue_A = 0.3;
float $shoulderL_rz_armpitL_ty_result = (shoulderL_jnt.rotateZ - $shoulderL_rz_init) * $shoulderL_armpitL_ty_subvalue_A;

float $armL_armpitL_ty_subvalue_A = 0.16;
float $armL_rz_armpitL_ty_result = (armL_jnt.rotateZ - $armL_rz_init) * $armL_armpitL_ty_subvalue_A;

float $armpitL_ty_subvalue_init = -14.635;
armpitL_subjnt.translateY = clamp(-14.635, -7, ($shoulderL_rz_armpitL_ty_result + $armL_rz_armpitL_ty_result) / 2 + $armpitL_ty_subvalue_init);

// armpitL tz
float $shoulderL_armpitL_tz_subvalue_A = -0.05751;
float $shoulderL_rz_armpitL_tz_result = (shoulderL_jnt.rotateZ - $shoulderL_rz_init) * $shoulderL_armpitL_tz_subvalue_A;

float $armL_armpitL_tz_subvalue_A = 0.00001;
float $armL_rz_armpitL_tz_result = (armL_jnt.rotateZ - $armL_rz_init) * $armL_armpitL_tz_subvalue_A;

float $armpitL_tz_subvalue_init = 3.863;
armpitL_subjnt.translateZ = ($shoulderL_rz_armpitL_tz_result + $armL_rz_armpitL_tz_result) / 2 + $armpitL_tz_subvalue_init;


// R init rotate
float $shoulderR_rz_init = 0.0;
float $armR_rz_init = -55.0;

// armpitR tx
float $shoulderR_armpitR_tx_subvalue_A = 0.1;
float $shoulderR_rz_armpitR_tx_result = (shoulderR_jnt.rotateZ - $shoulderR_rz_init) * $shoulderR_armpitR_tx_subvalue_A;

float $armR_armpitR_tx_subvalue_A = 0.1;
float $armR_rz_armpitR_tx_result = (armR_jnt.rotateZ - $armR_rz_init) * $armR_armpitR_tx_subvalue_A;

float $armpitR_tx_subvalue_init = -9.23725;
armpitR_subjnt.translateX = clamp(-12, 0, ($shoulderR_rz_armpitR_tx_result + $armR_rz_armpitR_tx_result) / 2 + $armpitR_tx_subvalue_init);

// armpitR ty
float $shoulderR_armpitR_ty_subvalue_A = -0.3;
float $shoulderR_rz_armpitR_ty_result = (shoulderR_jnt.rotateZ - $shoulderR_rz_init) * $shoulderR_armpitR_ty_subvalue_A;

float $armR_armpitR_ty_subvalue_A = -0.16;
float $armR_rz_armpitR_ty_result = (armR_jnt.rotateZ - $armR_rz_init) * $armR_armpitR_ty_subvalue_A;

float $armpitR_ty_subvalue_init = 14.635;
armpitR_subjnt.translateY = clamp(7, 14.635, ($shoulderR_rz_armpitR_ty_result + $armR_rz_armpitR_ty_result) / 2 + $armpitR_ty_subvalue_init);

// armpitR tz
float $shoulderR_armpitR_tz_subvalue_A = 0.05751;
float $shoulderR_rz_armpitR_tz_result = (shoulderR_jnt.rotateZ - $shoulderR_rz_init) * $shoulderR_armpitR_tz_subvalue_A;

float $armR_armpitR_tz_subvalue_A = -0.00001;
float $armR_rz_armpitR_tz_result = (armR_jnt.rotateZ - $armR_rz_init) * $armR_armpitR_tz_subvalue_A;

float $armpitR_tz_subvalue_init = -3.863;
armpitR_subjnt.translateZ = ($shoulderR_rz_armpitR_tz_result + $armR_rz_armpitR_tz_result) / 2 + $armpitR_tz_subvalue_init;

""", n='{0}'.format(exp_name), ae=0)


exp_name = 'elbow_subjnt_exp'
cmds.expression(s="""
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

proc float[] toQuaternion(float $yaw_z, float $pitch_y, float $roll_x){
    // yaw (Z), pitch (Y), roll (X)
    $yaw = convert_to_radians($yaw_z);
    $pitch = convert_to_radians($pitch_y);
    $roll = convert_to_radians($roll_x);

    float $cy = cos($yaw * 0.5);
    float $sy = sin($yaw * 0.5);
    float $cp = cos($pitch * 0.5);
    float $sp = sin($pitch * 0.5);
    float $cr = cos($roll * 0.5);
    float $sr = sin($roll * 0.5);

    float $qurt[];

    float $qw = $cy * $cp * $cr + $sy * $sp * $sr;
    float $qx = $cy * $cp * $sr - $sy * $sp * $cr;
    float $qy = $sy * $cp * $sr + $cy * $sp * $cr;
    float $qz = $sy * $cp * $cr - $cy * $sp * $sr;

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

    $euler[0] = atan2($sinr_cosp, $cosr_cosp);

    // pitch (y-axis rotation)
    float $sinp = 2 * ($quartw * $quarty - $quartz * $quartx);
    float $pi = 3.1415927;
    if (abs($sinp) >= 1){
        $euler[1] = -1 * $pi / 2;
    }
    else{
        $euler[1] = asin($sinp);
    }

    // yaw (z-axis rotation)
    float $siny_cosp = 2 * ($quartw * $quartz + $quartx * $quarty);
    float $cosy_cosp = 1 - 2 * ($quarty * $quarty + $quartz * $quartz);
    $euler[2] = atan2($siny_cosp, $cosy_cosp);

    return $euler;
}

proc float[] eulerToQuaternionToEuler(float $roll, float $pitch, float $yaw){
	float $e2q2e[];

	float $quartd[] = toQuaternion($yaw, $pitch, $roll);
	float $eulerd[] = toEuler($quartd[0], $quartd[1], $quartd[2], $quartd[3]);

	$e2q2e[0]=convert_to_degrees($eulerd[0]);
	$e2q2e[1]=convert_to_degrees($eulerd[1]);
	$e2q2e[2]=convert_to_degrees($eulerd[2]);

	return $e2q2e;

}

proc float relax_gimbal_rotation(float $pitchRot, float $srcRot, float $dstRot, float $ratio){
	// float $ratio = 90; // Pitch
	// float $pitchRot = uplegL_subjnt_3.rotateY;
	float $relax = 1 - abs($pitchRot) / $ratio;

	if ($srcRot > 90)
	{
		$dstRot = (180 - $srcRot) * $relax;
	}
	else if ($srcRot < -90)
	{
		$dstRot = -(180 + $srcRot) * $relax;
	}
	else
		$dstRot = $srcRot * $relax;

	return $dstRot;

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

// Left
float $eulerd_L[] = eulerToQuaternionToEuler(forearmL_jnt.rotateX, forearmL_jnt.rotateY, forearmL_jnt.rotateZ); // (Roll, Pitch, Yaw);
float $elbowL = $eulerd_L[1];
float $elbowL_tx_subvalue_A = 25.714;
float $elbowL_tz_subvalue_A = 60.0;
float $elbowL_ry_subvalue_A = -2.0;
elbowL_subjnt.translateX = $elbowL / $elbowL_tx_subvalue_A;
elbowL_subjnt.translateZ = $elbowL / $elbowL_tz_subvalue_A + -2;
elbowL_subjnt.rotateY = $elbowL / $elbowL_ry_subvalue_A;

float $elbowL_tz_subvalue_B = ($elbowL + 90.0)*0.06364;
float $elbowL_ry_subvalue_B = ($elbowL + 90.0)*-0.63637;
if (forearmL_jnt.rotateY < -90){
	elbowL_subjnt.translateX = -3.5;
	elbowL_subjnt.translateZ = -3.5 - $elbowL_tz_subvalue_B;
	elbowL_subjnt.rotateY = 45 + $elbowL_ry_subvalue_B;

}


// Right
float $eulerd_R[] = eulerToQuaternionToEuler(forearmR_jnt.rotateX, forearmR_jnt.rotateY, forearmR_jnt.rotateZ); // (Roll, Pitch, Yaw);
float $elbowR = $eulerd_R[1];
float $elbowR_tx_subvalue_A = -25.714;
float $elbowR_tz_subvalue_A = -60.0;
float $elbowR_ry_subvalue_A = -2.0;
elbowR_subjnt.translateX = $elbowR / $elbowR_tx_subvalue_A;
elbowR_subjnt.translateZ = $elbowR / $elbowR_tz_subvalue_A + 2;
elbowR_subjnt.rotateY = $elbowR / $elbowR_ry_subvalue_A;

float $elbowR_tz_subvalue_B = ($elbowR + 90.0)*-0.06364;
float $elbowR_ry_subvalue_B = ($elbowR + 90.0)*-0.63637;
if (forearmR_jnt.rotateY < -90){
	elbowR_subjnt.translateX = 3.5;
	elbowR_subjnt.translateZ = 3.5 - $elbowR_tz_subvalue_B;
	elbowR_subjnt.rotateY = 45 + $elbowR_ry_subvalue_B;

}
""", n='{0}'.format(exp_name), ae=0)
