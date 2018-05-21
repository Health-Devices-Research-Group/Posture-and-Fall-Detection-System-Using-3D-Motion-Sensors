#include <iostream>
#include <Kinect.h>
#include <fstream>
#include <math.h>
#include <string.h>
#include <string>
#include <chrono>

#define PI 3.14159265

int num_frames = 0;
long long fileName = 0;

void processBodies(const unsigned int &bodyCount, IBody **bodies);

template<class Interface>
static inline void safeRelease(Interface *&interfaceToRelease)
{
	if (interfaceToRelease != nullptr) {
		interfaceToRelease->Release();
		interfaceToRelease = nullptr;
	}
}

int main(int argc, char *argv[])
{
	
	IKinectSensor *sensor = nullptr;
	IBodyFrameReader *bodyFrameReader = nullptr;

	//Get the default Kinect sensor
	HRESULT hr = GetDefaultKinectSensor(&sensor);

	//If the function succeeds, open the sensor
	if (SUCCEEDED(hr)) {
		std::cout << "Sensor detected!\n";
		hr = sensor->Open();

		if (SUCCEEDED(hr)) {
			//Get a body frame source from which we can get our body frame reader
			IBodyFrameSource *bodyFrameSource = nullptr;
			hr = sensor->get_BodyFrameSource(&bodyFrameSource);

			if (SUCCEEDED(hr)) {
				hr = bodyFrameSource->OpenReader(&bodyFrameReader);
			}

			//We're done with bodyFrameSource, so we'll release it
			safeRelease(bodyFrameSource);
		}
	}

	if (sensor == nullptr || FAILED(hr)) {
		std::cerr << "Cannot find any sensors.\n";
		return E_FAIL;
	}

	while (bodyFrameReader != nullptr) {
		IBodyFrame *bodyFrame = nullptr;
		hr = bodyFrameReader->AcquireLatestFrame(&bodyFrame);

		if (SUCCEEDED(hr)) {
			IBody *bodies[BODY_COUNT] = { 0 };
			hr = bodyFrame->GetAndRefreshBodyData(_countof(bodies), bodies);

			if (SUCCEEDED(hr)) {
				if (fileName == 0 || fileName + 60000 < std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count()) {
					fileName = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count();
				}
				processBodies(BODY_COUNT, bodies);
				//After body processing is done, we're done with our bodies so release them.
				for (unsigned int bodyIndex = 0; bodyIndex < _countof(bodies); bodyIndex++) {
					safeRelease(bodies[bodyIndex]);
				}

				safeRelease(bodyFrame);
			}
		}
		else if (sensor) {
			BOOLEAN isSensorAvailable = false;
			hr = sensor->get_IsAvailable(&isSensorAvailable);
			if (SUCCEEDED(hr) && isSensorAvailable == false) {
				std::cerr << "No available sensor is found.\n";
			}
		}
		else {
			std::cerr << "Trouble reading the body frame.\n";
		}
	}

	return 0;
}

void processBodies(const unsigned int &bodyCount, IBody **bodies)
{

	//File where to write the XYZ coords pf the skeleton joints.
	std::ofstream dataFile;
	//dataFile.open("joints_data_standing.txt", std::ofstream::out | std::ofstream::app);
	dataFile.open("real_time_joints_data.txt", std::ofstream::out | std::ofstream::app);
	if (!dataFile) { //create file if not exists
		dataFile.open("joints_data.txt", std::ofstream::out, std::ofstream::trunc);
	}

	//Record 1 minute data in this file
	std::ofstream oneMinuteFile;
	oneMinuteFile.open("C:\\workspace\\FallDetection\\src\\data\\" + std::to_string(fileName) + ".txt", std::ofstream::out | std::ofstream::app);
	if (!oneMinuteFile) { //create file if not exists
		oneMinuteFile.open("C:\\workspace\\FallDetection\\src\\data\\" + std::to_string(fileName) + ".txt", std::ofstream::out, std::ofstream::trunc);
	}

	for (unsigned int bodyIndex = 0; bodyIndex < bodyCount; bodyIndex++) { 
		IBody *body = bodies[bodyIndex];

		//Get the tracking status for the body, if it's not tracked we'll skip it
		BOOLEAN isTracked = false;
		HRESULT hr = body->get_IsTracked(&isTracked);
		if (FAILED(hr) || isTracked == false) {
			continue;
		}

		//If we're here the body is tracked so lets get the joint properties for this skeleton
		Joint joints[JointType_Count];
		hr = body->GetJoints(_countof(joints), joints);
		if (SUCCEEDED(hr)) {
			if (num_frames % 3 == 0) { //Make it 10FPS instead of 30 (divide ratio of 3)
				//Get the 25 skeleton joints!
				const CameraSpacePoint &spineBasePos = joints[JointType_SpineBase].Position;
				const CameraSpacePoint &spineMidPos = joints[JointType_SpineMid].Position;
				const CameraSpacePoint &neckPos = joints[JointType_Neck].Position;
				const CameraSpacePoint &headPos = joints[JointType_Head].Position;
				const CameraSpacePoint &shoulderLeftPos = joints[JointType_ShoulderLeft].Position;

				const CameraSpacePoint &elbowLeftPos = joints[JointType_ElbowLeft].Position;
				const CameraSpacePoint &wristLeftPos = joints[JointType_WristLeft].Position;
				const CameraSpacePoint &handLeftPos = joints[JointType_HandLeft].Position;
				const CameraSpacePoint &shoulderRightPos = joints[JointType_ShoulderRight].Position;
				const CameraSpacePoint &elbowRightPos = joints[JointType_ElbowRight].Position;

				const CameraSpacePoint &wristRightPos = joints[JointType_WristRight].Position;
				const CameraSpacePoint &handRightPos = joints[JointType_HandRight].Position;
				const CameraSpacePoint &hipLeftPos = joints[JointType_HipLeft].Position;
				const CameraSpacePoint &kneeLeftPos = joints[JointType_KneeLeft].Position;
				const CameraSpacePoint &ankleLeftPos = joints[JointType_AnkleLeft].Position;

				const CameraSpacePoint &footLeftPos = joints[JointType_FootLeft].Position;
				const CameraSpacePoint &hipRightPos = joints[JointType_HipRight].Position;
				const CameraSpacePoint &kneeRightPos = joints[JointType_KneeRight].Position;
				const CameraSpacePoint &ankleRightPos = joints[JointType_AnkleRight].Position;
				const CameraSpacePoint &footRightPos = joints[JointType_FootRight].Position;

				const CameraSpacePoint &spineShoulderPos = joints[JointType_SpineShoulder].Position;
				const CameraSpacePoint &handTipLeftPos = joints[JointType_HandTipLeft].Position;
				const CameraSpacePoint &thumbLeftPos = joints[JointType_ThumbLeft].Position;
				const CameraSpacePoint &handTipRightPos = joints[JointType_HandTipRight].Position;
				const CameraSpacePoint &thumbRightPos = joints[JointType_ThumbRight].Position;

				//distances between joints
				float a = sqrt(pow(hipLeftPos.X - kneeLeftPos.X, 2) + pow(hipLeftPos.Y - kneeLeftPos.Y, 2) + pow(hipLeftPos.Z - kneeLeftPos.Z, 2));
				float b = sqrt(pow(spineBasePos.X - hipLeftPos.X, 2) + pow(spineBasePos.Y - hipLeftPos.Y, 2) + pow(spineBasePos.Z - hipLeftPos.Z, 2));
				float c = sqrt(pow(spineBasePos.X - kneeLeftPos.X, 2) + pow(spineBasePos.Y - kneeLeftPos.Y, 2) + pow(spineBasePos.Z - kneeLeftPos.Z, 2));

				float d = sqrt(pow(hipRightPos.X - kneeRightPos.X, 2) + pow(hipRightPos.Y - kneeRightPos.Y, 2) + pow(hipRightPos.Z - kneeRightPos.Z, 2));
				float e = sqrt(pow(spineBasePos.X - hipRightPos.X, 2) + pow(spineBasePos.Y - hipRightPos.Y, 2) + pow(spineBasePos.Z - hipRightPos.Z, 2));
				float f = sqrt(pow(spineBasePos.X - kneeRightPos.X, 2) + pow(spineBasePos.Y - kneeRightPos.Y, 2) + pow(spineBasePos.Z - kneeRightPos.Z, 2));

				float g = sqrt(pow(hipLeftPos.X - ankleLeftPos.X, 2) + pow(hipLeftPos.Y - ankleLeftPos.Y, 2) + pow(hipLeftPos.Z - ankleLeftPos.Z, 2));
				float h = sqrt(pow(kneeLeftPos.X - ankleLeftPos.X, 2) + pow(kneeLeftPos.Y - ankleLeftPos.Y, 2) + pow(kneeLeftPos.Z - ankleLeftPos.Z, 2));

				float i = sqrt(pow(hipRightPos.X - ankleRightPos.X, 2) + pow(hipRightPos.Y - ankleRightPos.Y, 2) + pow(hipRightPos.Z - ankleRightPos.Z, 2));
				float j = sqrt(pow(kneeRightPos.X - ankleRightPos.X, 2) + pow(kneeRightPos.Y - ankleRightPos.Y, 2) + pow(kneeRightPos.Z - ankleRightPos.Z, 2));

				float k = sqrt(pow(kneeLeftPos.X - footLeftPos.X, 2) + pow(kneeLeftPos.Y - footLeftPos.Y, 2) + pow(kneeLeftPos.Z - footLeftPos.Z, 2));
				float l = sqrt(pow(ankleLeftPos.X - footLeftPos.X, 2) + pow(ankleLeftPos.Y - footLeftPos.Y, 2) + pow(ankleLeftPos.Z - footLeftPos.Z, 2));

				float m = sqrt(pow(kneeRightPos.X - footRightPos.X, 2) + pow(kneeRightPos.Y - footRightPos.Y, 2) + pow(kneeRightPos.Z - footRightPos.Z, 2));
				float n = sqrt(pow(ankleRightPos.X - footRightPos.X, 2) + pow(ankleRightPos.Y - footRightPos.Y, 2) + pow(ankleRightPos.Z - footRightPos.Z, 2));

				float o = sqrt(pow((0.5*ankleLeftPos.X + 0.5*ankleRightPos.X) - footLeftPos.X, 2) + pow(ankleLeftPos.Z - footLeftPos.Z, 2));
				float p = sqrt(pow((0.5*ankleLeftPos.X + 0.5*ankleRightPos.X) - footRightPos.X, 2) + pow(ankleRightPos.Z - footRightPos.Z, 2));
				float q = sqrt(pow(footLeftPos.X - footRightPos.X, 2) + pow(footLeftPos.Y - footRightPos.Y, 2) + pow(footLeftPos.Z - footRightPos.Z, 2));

				//remove these
				//float r = sqrt(pow(spineMidPos.X - spineBasePos.X, 2) + pow(spineMidPos.Y - spineBasePos.Y, 2) + pow(spineMidPos.Z - spineBasePos.Z, 2));
				//float s = sqrt(pow(spineShoulderPos.X - spineMidPos.X, 2) + pow(spineShoulderPos.Y - spineMidPos.Y, 2) + pow(spineShoulderPos.Z - spineMidPos.Z, 2));

				float r = sqrt(pow(spineBasePos.X - spineShoulderPos.X, 2) + pow(spineBasePos.Z - spineShoulderPos.Z, 2));
				float s = sqrt(r + pow(spineShoulderPos.Y - spineBasePos.Y, 2));
				float t = sqrt(pow(spineShoulderPos.X - spineBasePos.X, 2) + pow(spineShoulderPos.Y - spineBasePos.Y, 2) + pow(spineShoulderPos.Z - spineBasePos.Z, 2));

				float u = sqrt(pow(spineShoulderPos.X - ((kneeLeftPos.X + kneeRightPos.X) / 2), 2) + pow(spineShoulderPos.Y - ((kneeLeftPos.Y + kneeRightPos.Y) / 2), 2) + pow(spineShoulderPos.Z - ((kneeLeftPos.Z + kneeRightPos.Z) / 2), 2));
				float v = sqrt(pow(spineBasePos.X - ((kneeLeftPos.X + kneeRightPos.X) / 2), 2) + pow(spineBasePos.Y - ((kneeLeftPos.Y + kneeRightPos.Y) / 2), 2) + pow(spineBasePos.Z - ((kneeLeftPos.Z + kneeRightPos.Z) / 2), 2));

				//8 features from body joints
				float height = headPos.Y - std::fmin(footLeftPos.Y, footRightPos.Y);
				float leftHipAngle = acos((pow(a, 2) + pow(b, 2) - pow(c, 2)) / (2 * a*b)) * 180 / PI;  //180 - (acos(a/c) *180.0 / PI) - (acos(b/c) *180.0 / PI);
				float rightHipAngle = acos((pow(e, 2) + pow(d, 2) - pow(f, 2)) / (2 * e*d)) * 180 / PI; // 180 - (acos(d / f) *180.0 / PI) - (acos(e / f) *180.0 / PI);
				float leftKneeAngle = acos((pow(a, 2) + pow(h, 2) - pow(g, 2)) / (2 * a*h)) * 180 / PI; // 180 - (acos(a / g) *180.0 / PI) - (acos(h / g) *180.0 / PI);
				float rightKneeAngle = acos((pow(d, 2) + pow(j, 2) - pow(i, 2)) / (2 * d*j)) * 180 / PI; // 180 - (acos(d / i) *180.0 / PI) - (acos(j / i) *180.0 / PI);

				//float leftAnkleAngle = acos((pow(h, 2) + pow(l, 2) - pow(k, 2)) / (2 * h*l)) * 180 / PI; // 180 - (acos(h / k) *180.0 / PI) - (acos(l / k) *180.0 / PI);
				//float rightAnkleAngle = acos((pow(j, 2) + pow(n, 2) - pow(m, 2)) / (2 * j*n)) * 180 / PI;  // 180 - (acos(j / m) *180.0 / PI) - (acos(n / m) *180.0 / PI);
				//float twoFeetAngle = acos((pow(o, 2) + pow(p, 2) - pow(q, 2)) / (2 * o*p)) * 180 / PI; // 180 - (acos(o / q) *180.0 / PI) - (acos(p / q) *180.0 / PI);

				float chestAngle = 180 - (acos((pow(t, 2) + pow(s, 2) - pow(r, 2)) / (2 * t*s)) * 180 / PI); //acos((pow(r, 2) + pow(s, 2) - pow(t, 2)) / (2 * r*s)) * 180 / PI;
				float chestKneeAngle = acos((pow(t, 2) + pow(v, 2) - pow(u, 2)) / (2 * t*v)) * 180 / PI;

				//Prints the joints coords in the data file if data is not 'nan'
				if (height == height && leftHipAngle == leftHipAngle && rightHipAngle == rightHipAngle && leftKneeAngle == leftKneeAngle
					&& rightKneeAngle == rightKneeAngle && chestAngle == chestAngle && chestKneeAngle == chestKneeAngle && footRightPos.Y == footRightPos.Y
					&& footLeftPos.Y == footLeftPos.Y) {
					dataFile << height << "\n";
					dataFile << leftHipAngle << "\n";
					dataFile << rightHipAngle << "\n";
					dataFile << leftKneeAngle << "\n";
					dataFile << rightKneeAngle << "\n";
					dataFile << chestAngle << "\n";
					dataFile << chestKneeAngle << "\n";
					//these two are only for the real time application!
					dataFile << footRightPos.Y << "\n";
					dataFile << footLeftPos.Y << "\n";
					//frame timestamp
					dataFile << std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count() << "\n";
				}
			}
			num_frames++; //only if succeeded to retrieve body joints!
		}
	}
	dataFile.close();
}