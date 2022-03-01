(define (problem roverprob5621  )   (:domain Rover  )  
(:objects
general - Lander
colour high_res low_res - Mode
rover0 - Rover
rover0store - Store
waypoint0 waypoint1 waypoint2 waypoint3 waypoint4 waypoint5 waypoint6 waypoint7 waypoint8 waypoint9 waypoint25 waypoint26 waypoint27 waypoint28 waypoint29 waypoint30 waypoint31 waypoint32 waypoint33 waypoint34 waypoint35 waypoint36 waypoint37 waypoint38 waypoint39 waypoint40 waypoint41 waypoint42 waypoint43 waypoint44 waypoint45 waypoint46 waypoint47 waypoint48 waypoint49 - Waypoint
camera0 camera1 camera2 camera3 camera4 camera5 camera6 camera7 camera8 camera9 camera10 camera11 camera12 camera13 - Camera
objective0 objective1 objective2 objective3 objective4 objective5 objective6 objective7 - Objective
)
(:init
	(visible waypoint0 waypoint4  )  
	(visible waypoint4 waypoint0  )  
	(visible waypoint0 waypoint5  )  
	(visible waypoint5 waypoint0  )  
	(visible waypoint0 waypoint6  )  
	(visible waypoint6 waypoint0  )  
	(visible waypoint0 waypoint9  )  
	(visible waypoint9 waypoint0  )  
	(visible waypoint0 waypoint29  )  
	(visible waypoint29 waypoint0  )  
	(visible waypoint1 waypoint29  )  
	(visible waypoint29 waypoint1  )  
	(visible waypoint1 waypoint35  )  
	(visible waypoint35 waypoint1  )  
	(visible waypoint1 waypoint43  )  
	(visible waypoint43 waypoint1  )  
	(visible waypoint2 waypoint33  )  
	(visible waypoint33 waypoint2  )  
	(visible waypoint2 waypoint42  )  
	(visible waypoint42 waypoint2  )  
	(visible waypoint3 waypoint4  )  
	(visible waypoint4 waypoint3  )  
	(visible waypoint3 waypoint8  )  
	(visible waypoint8 waypoint3  )  
	(visible waypoint3 waypoint32  )  
	(visible waypoint32 waypoint3  )  
	(visible waypoint3 waypoint43  )  
	(visible waypoint43 waypoint3  )  
	(visible waypoint4 waypoint43  )  
	(visible waypoint43 waypoint4  )  
	(visible waypoint5 waypoint25  )  
	(visible waypoint25 waypoint5  )  
	(visible waypoint5 waypoint40  )  
	(visible waypoint40 waypoint5  )  
	(visible waypoint6 waypoint47  )  
	(visible waypoint47 waypoint6  )  
	(visible waypoint7 waypoint30  )  
	(visible waypoint30 waypoint7  )  
	(visible waypoint7 waypoint40  )  
	(visible waypoint40 waypoint7  )  
	(visible waypoint7 waypoint49  )  
	(visible waypoint49 waypoint7  )  
	(visible waypoint8 waypoint43  )  
	(visible waypoint43 waypoint8  )  
	(visible waypoint9 waypoint2  )  
	(visible waypoint2 waypoint9  )  
	(visible waypoint9 waypoint6  )  
	(visible waypoint6 waypoint9  )  
	(visible waypoint9 waypoint33  )  
	(visible waypoint33 waypoint9  )  
	(visible waypoint9 waypoint34  )  
	(visible waypoint34 waypoint9  )  
	(visible waypoint9 waypoint35  )  
	(visible waypoint35 waypoint9  )  
	(visible waypoint9 waypoint41  )  
	(visible waypoint41 waypoint9  )  
	(visible waypoint25 waypoint6  )  
	(visible waypoint6 waypoint25  )  
	(visible waypoint25 waypoint28  )  
	(visible waypoint28 waypoint25  )  
	(visible waypoint25 waypoint35  )  
	(visible waypoint35 waypoint25  )  
	(visible waypoint25 waypoint36  )  
	(visible waypoint36 waypoint25  )  
	(visible waypoint26 waypoint0  )  
	(visible waypoint0 waypoint26  )  
	(visible waypoint26 waypoint9  )  
	(visible waypoint9 waypoint26  )  
	(visible waypoint26 waypoint25  )  
	(visible waypoint25 waypoint26  )  
	(visible waypoint26 waypoint44  )  
	(visible waypoint44 waypoint26  )  
	(visible waypoint27 waypoint32  )  
	(visible waypoint32 waypoint27  )  
	(visible waypoint27 waypoint33  )  
	(visible waypoint33 waypoint27  )  
	(visible waypoint27 waypoint34  )  
	(visible waypoint34 waypoint27  )  
	(visible waypoint28 waypoint0  )  
	(visible waypoint0 waypoint28  )  
	(visible waypoint29 waypoint34  )  
	(visible waypoint34 waypoint29  )  
	(visible waypoint29 waypoint39  )  
	(visible waypoint39 waypoint29  )  
	(visible waypoint29 waypoint41  )  
	(visible waypoint41 waypoint29  )  
	(visible waypoint30 waypoint3  )  
	(visible waypoint3 waypoint30  )  
	(visible waypoint30 waypoint5  )  
	(visible waypoint5 waypoint30  )  
	(visible waypoint30 waypoint8  )  
	(visible waypoint8 waypoint30  )  
	(visible waypoint30 waypoint28  )  
	(visible waypoint28 waypoint30  )  
	(visible waypoint30 waypoint33  )  
	(visible waypoint33 waypoint30  )  
	(visible waypoint30 waypoint45  )  
	(visible waypoint45 waypoint30  )  
	(visible waypoint31 waypoint35  )  
	(visible waypoint35 waypoint31  )  
	(visible waypoint31 waypoint41  )  
	(visible waypoint41 waypoint31  )  
	(visible waypoint32 waypoint34  )  
	(visible waypoint34 waypoint32  )  
	(visible waypoint32 waypoint36  )  
	(visible waypoint36 waypoint32  )  
	(visible waypoint32 waypoint49  )  
	(visible waypoint49 waypoint32  )  
	(visible waypoint33 waypoint0  )  
	(visible waypoint0 waypoint33  )  
	(visible waypoint33 waypoint44  )  
	(visible waypoint44 waypoint33  )  
	(visible waypoint34 waypoint1  )  
	(visible waypoint1 waypoint34  )  
	(visible waypoint35 waypoint4  )  
	(visible waypoint4 waypoint35  )  
	(visible waypoint35 waypoint28  )  
	(visible waypoint28 waypoint35  )  
	(visible waypoint35 waypoint37  )  
	(visible waypoint37 waypoint35  )  
	(visible waypoint36 waypoint2  )  
	(visible waypoint2 waypoint36  )  
	(visible waypoint36 waypoint37  )  
	(visible waypoint37 waypoint36  )  
	(visible waypoint36 waypoint38  )  
	(visible waypoint38 waypoint36  )  
	(visible waypoint37 waypoint8  )  
	(visible waypoint8 waypoint37  )  
	(visible waypoint37 waypoint30  )  
	(visible waypoint30 waypoint37  )  
	(visible waypoint37 waypoint32  )  
	(visible waypoint32 waypoint37  )  
	(visible waypoint37 waypoint34  )  
	(visible waypoint34 waypoint37  )  
	(visible waypoint37 waypoint46  )  
	(visible waypoint46 waypoint37  )  
	(visible waypoint38 waypoint3  )  
	(visible waypoint3 waypoint38  )  
	(visible waypoint39 waypoint25  )  
	(visible waypoint25 waypoint39  )  
	(visible waypoint39 waypoint26  )  
	(visible waypoint26 waypoint39  )  
	(visible waypoint39 waypoint36  )  
	(visible waypoint36 waypoint39  )  
	(visible waypoint40 waypoint37  )  
	(visible waypoint37 waypoint40  )  
	(visible waypoint41 waypoint1  )  
	(visible waypoint1 waypoint41  )  
	(visible waypoint41 waypoint34  )  
	(visible waypoint34 waypoint41  )  
	(visible waypoint41 waypoint35  )  
	(visible waypoint35 waypoint41  )  
	(visible waypoint41 waypoint39  )  
	(visible waypoint39 waypoint41  )  
	(visible waypoint42 waypoint31  )  
	(visible waypoint31 waypoint42  )  
	(visible waypoint42 waypoint36  )  
	(visible waypoint36 waypoint42  )  
	(visible waypoint42 waypoint39  )  
	(visible waypoint39 waypoint42  )  
	(visible waypoint42 waypoint41  )  
	(visible waypoint41 waypoint42  )  
	(visible waypoint42 waypoint44  )  
	(visible waypoint44 waypoint42  )  
	(visible waypoint43 waypoint7  )  
	(visible waypoint7 waypoint43  )  
	(visible waypoint43 waypoint37  )  
	(visible waypoint37 waypoint43  )  
	(visible waypoint43 waypoint42  )  
	(visible waypoint42 waypoint43  )  
	(visible waypoint44 waypoint8  )  
	(visible waypoint8 waypoint44  )  
	(visible waypoint44 waypoint30  )  
	(visible waypoint30 waypoint44  )  
	(visible waypoint44 waypoint49  )  
	(visible waypoint49 waypoint44  )  
	(visible waypoint45 waypoint27  )  
	(visible waypoint27 waypoint45  )  
	(visible waypoint45 waypoint39  )  
	(visible waypoint39 waypoint45  )  
	(visible waypoint45 waypoint47  )  
	(visible waypoint47 waypoint45  )  
	(visible waypoint46 waypoint43  )  
	(visible waypoint43 waypoint46  )  
	(visible waypoint46 waypoint47  )  
	(visible waypoint47 waypoint46  )  
	(visible waypoint46 waypoint48  )  
	(visible waypoint48 waypoint46  )  
	(visible waypoint47 waypoint3  )  
	(visible waypoint3 waypoint47  )  
	(visible waypoint47 waypoint9  )  
	(visible waypoint9 waypoint47  )  
	(visible waypoint47 waypoint25  )  
	(visible waypoint25 waypoint47  )  
	(visible waypoint48 waypoint6  )  
	(visible waypoint6 waypoint48  )  
	(visible waypoint48 waypoint26  )  
	(visible waypoint26 waypoint48  )  
	(at_soil_sample waypoint0  )  
	(at_rock_sample waypoint0  )  
	(at_soil_sample waypoint1  )  
	(at_rock_sample waypoint1  )  
	(at_rock_sample waypoint2  )  
	(at_soil_sample waypoint3  )  
	(at_soil_sample waypoint4  )  
	(at_rock_sample waypoint7  )  
	(at_soil_sample waypoint8  )  
	(at_soil_sample waypoint25  )  
	(at_soil_sample waypoint26  )  
	(at_soil_sample waypoint31  )  
	(at_rock_sample waypoint31  )  
	(at_soil_sample waypoint32  )  
	(at_rock_sample waypoint32  )  
	(at_soil_sample waypoint33  )  
	(at_rock_sample waypoint33  )  
	(at_soil_sample waypoint34  )  
	(at_rock_sample waypoint34  )  
	(at_soil_sample waypoint35  )  
	(at_rock_sample waypoint35  )  
	(at_rock_sample waypoint36  )  
	(at_soil_sample waypoint37  )  
	(at_rock_sample waypoint37  )  
	(at_soil_sample waypoint38  )  
	(at_rock_sample waypoint38  )  
	(at_soil_sample waypoint39  )  
	(at_soil_sample waypoint41  )  
	(at_rock_sample waypoint42  )  
	(at_rock_sample waypoint43  )  
	(at_rock_sample waypoint44  )  
	(at_soil_sample waypoint45  )  
	(at_soil_sample waypoint46  )  
	(at_soil_sample waypoint47  )  
	(at_soil_sample waypoint48  )  
	(at_rock_sample waypoint48  )  
	(at_soil_sample waypoint49  )  
	(at_lander general waypoint36  )  
	(channel_free general  )  
	(at rover0 waypoint0  )  
	(available rover0  )  
	(store_of rover0store rover0  )  
	(empty rover0store  )  
	(equipped_for_rock_analysis rover0  )  
	(equipped_for_imaging rover0  )  
	(can_traverse rover0 waypoint0 waypoint4  )  
	(can_traverse rover0 waypoint4 waypoint0  )  
	(can_traverse rover0 waypoint0 waypoint5  )  
	(can_traverse rover0 waypoint5 waypoint0  )  
	(can_traverse rover0 waypoint0 waypoint6  )  
	(can_traverse rover0 waypoint6 waypoint0  )  
	(can_traverse rover0 waypoint0 waypoint26  )  
	(can_traverse rover0 waypoint26 waypoint0  )  
	(can_traverse rover0 waypoint0 waypoint28  )  
	(can_traverse rover0 waypoint28 waypoint0  )  
	(can_traverse rover0 waypoint0 waypoint29  )  
	(can_traverse rover0 waypoint29 waypoint0  )  
	(can_traverse rover0 waypoint0 waypoint33  )  
	(can_traverse rover0 waypoint33 waypoint0  )  
	(can_traverse rover0 waypoint4 waypoint3  )  
	(can_traverse rover0 waypoint3 waypoint4  )  
	(can_traverse rover0 waypoint5 waypoint25  )  
	(can_traverse rover0 waypoint25 waypoint5  )  
	(can_traverse rover0 waypoint5 waypoint30  )  
	(can_traverse rover0 waypoint30 waypoint5  )  
	(can_traverse rover0 waypoint5 waypoint40  )  
	(can_traverse rover0 waypoint40 waypoint5  )  
	(can_traverse rover0 waypoint26 waypoint9  )  
	(can_traverse rover0 waypoint9 waypoint26  )  
	(can_traverse rover0 waypoint26 waypoint39  )  
	(can_traverse rover0 waypoint39 waypoint26  )  
	(can_traverse rover0 waypoint26 waypoint48  )  
	(can_traverse rover0 waypoint48 waypoint26  )  
	(can_traverse rover0 waypoint29 waypoint1  )  
	(can_traverse rover0 waypoint1 waypoint29  )  
	(can_traverse rover0 waypoint29 waypoint41  )  
	(can_traverse rover0 waypoint41 waypoint29  )  
	(can_traverse rover0 waypoint33 waypoint2  )  
	(can_traverse rover0 waypoint2 waypoint33  )  
	(can_traverse rover0 waypoint33 waypoint27  )  
	(can_traverse rover0 waypoint27 waypoint33  )  
	(can_traverse rover0 waypoint30 waypoint7  )  
	(can_traverse rover0 waypoint7 waypoint30  )  
	(can_traverse rover0 waypoint45 waypoint47  )  
	(can_traverse rover0 waypoint47 waypoint45  )  
	(on_board camera0 rover0  )  
	(calibration_target camera0 objective3  )  
	(supports camera0 colour  )  
	(supports camera0 high_res  )  
	(calibration_target camera1 objective7  )  
	(supports camera1 colour  )  
	(supports camera1 high_res  )  
	(calibration_target camera2 objective3  )  
	(supports camera2 high_res  )  
	(calibration_target camera3 objective6  )  
	(supports camera3 colour  )  
	(supports camera3 high_res  )  
	(supports camera3 low_res  )  
	(calibration_target camera4 objective1  )  
	(supports camera4 high_res  )  
	(calibration_target camera5 objective4  )  
	(supports camera5 low_res  )  
	(calibration_target camera6 objective3  )  
	(supports camera6 colour  )  
	(supports camera6 low_res  )  
	(calibration_target camera7 objective0  )  
	(supports camera7 low_res  )  
	(calibration_target camera8 objective1  )  
	(supports camera8 colour  )  
	(supports camera8 high_res  )  
	(supports camera8 low_res  )  
	(calibration_target camera9 objective5  )  
	(supports camera9 colour  )  
	(supports camera9 high_res  )  
	(supports camera9 low_res  )  
	(calibration_target camera10 objective1  )  
	(supports camera10 high_res  )  
	(supports camera10 low_res  )  
	(calibration_target camera11 objective7  )  
	(supports camera11 low_res  )  
	(calibration_target camera12 objective5  )  
	(supports camera12 colour  )  
	(supports camera12 low_res  )  
	(calibration_target camera13 objective0  )  
	(supports camera13 colour  )  
	(supports camera13 low_res  )  
	(visible_from objective0 waypoint0  )  
	(visible_from objective0 waypoint1  )  
	(visible_from objective0 waypoint2  )  
	(visible_from objective0 waypoint3  )  
	(visible_from objective0 waypoint4  )  
	(visible_from objective1 waypoint0  )  
	(visible_from objective1 waypoint1  )  
	(visible_from objective1 waypoint2  )  
	(visible_from objective1 waypoint3  )  
	(visible_from objective1 waypoint4  )  
	(visible_from objective1 waypoint5  )  
	(visible_from objective1 waypoint6  )  
	(visible_from objective1 waypoint7  )  
	(visible_from objective1 waypoint8  )  
	(visible_from objective1 waypoint9  )  
	(visible_from objective1 waypoint25  )  
	(visible_from objective1 waypoint26  )  
	(visible_from objective1 waypoint27  )  
	(visible_from objective1 waypoint28  )  
	(visible_from objective1 waypoint29  )  
	(visible_from objective1 waypoint30  )  
	(visible_from objective1 waypoint31  )  
	(visible_from objective1 waypoint32  )  
	(visible_from objective1 waypoint33  )  
	(visible_from objective1 waypoint34  )  
	(visible_from objective1 waypoint35  )  
	(visible_from objective1 waypoint36  )  
	(visible_from objective1 waypoint37  )  
	(visible_from objective1 waypoint38  )  
	(visible_from objective1 waypoint39  )  
	(visible_from objective1 waypoint40  )  
	(visible_from objective1 waypoint41  )  
	(visible_from objective2 waypoint0  )  
	(visible_from objective2 waypoint1  )  
	(visible_from objective2 waypoint2  )  
	(visible_from objective2 waypoint3  )  
	(visible_from objective2 waypoint4  )  
	(visible_from objective2 waypoint5  )  
	(visible_from objective2 waypoint6  )  
	(visible_from objective2 waypoint7  )  
	(visible_from objective2 waypoint8  )  
	(visible_from objective2 waypoint9  )  
	(visible_from objective3 waypoint0  )  
	(visible_from objective3 waypoint1  )  
	(visible_from objective3 waypoint2  )  
	(visible_from objective4 waypoint0  )  
	(visible_from objective4 waypoint1  )  
	(visible_from objective4 waypoint2  )  
	(visible_from objective4 waypoint3  )  
	(visible_from objective5 waypoint0  )  
	(visible_from objective5 waypoint1  )  
	(visible_from objective5 waypoint2  )  
	(visible_from objective5 waypoint3  )  
	(visible_from objective5 waypoint4  )  
	(visible_from objective5 waypoint5  )  
	(visible_from objective5 waypoint6  )  
	(visible_from objective5 waypoint7  )  
	(visible_from objective5 waypoint8  )  
	(visible_from objective5 waypoint9  )  
	(visible_from objective5 waypoint25  )  
	(visible_from objective5 waypoint26  )  
	(visible_from objective6 waypoint0  )  
	(visible_from objective6 waypoint1  )  
	(visible_from objective6 waypoint2  )  
	(visible_from objective6 waypoint3  )  
	(visible_from objective6 waypoint4  )  
	(visible_from objective6 waypoint5  )  
	(visible_from objective6 waypoint6  )  
	(visible_from objective6 waypoint7  )  
	(visible_from objective6 waypoint8  )  
	(visible_from objective6 waypoint9  )  
	(visible_from objective7 waypoint0  )  
	(visible_from objective7 waypoint1  )  
	(visible_from objective7 waypoint2  )  
	(visible_from objective7 waypoint3  )  
	(visible_from objective7 waypoint4  )  
	(visible_from objective7 waypoint5  )  
	(visible_from objective7 waypoint6  )  
	(visible_from objective7 waypoint7  )  
	(visible_from objective7 waypoint8  )  
	(visible_from objective7 waypoint9  )  
	(visible_from objective7 waypoint25  )  
	(visible_from objective7 waypoint26  )  
	(visible_from objective7 waypoint27  )  
	(visible_from objective7 waypoint28  )  
	(visible_from objective7 waypoint29  )  
	(visible_from objective7 waypoint30  )  
	(visible_from objective7 waypoint31  )  
	(visible_from objective7 waypoint32  )  
	(visible_from objective7 waypoint33  )  
	(visible_from objective7 waypoint34  )  
	(visible_from objective7 waypoint35  )  
	(visible_from objective7 waypoint36  )  
	(visible_from objective7 waypoint37  )  
	(visible_from objective7 waypoint38  )  
	(visible_from objective7 waypoint39  )  
	(visible_from objective7 waypoint40  )  
	(visible_from objective7 waypoint41  )  
	(visible_from objective7 waypoint42  )  
	(visible_from objective7 waypoint43  )  
  )  

(:goal (and
(communicated_soil_data waypoint46  )  
(communicated_soil_data waypoint1  )  
(communicated_soil_data waypoint39  )  
(communicated_soil_data waypoint31  )  
(communicated_soil_data waypoint45  )  
(communicated_soil_data waypoint49  )  
(communicated_soil_data waypoint41  )  
(communicated_soil_data waypoint25  )  
(communicated_rock_data waypoint48  )  
(communicated_rock_data waypoint1  )  
(communicated_rock_data waypoint2  )  
(communicated_rock_data waypoint43  )  
(communicated_image_data objective1 high_res  )  
(communicated_image_data objective6 high_res  )  
(communicated_image_data objective7 colour  )  
(communicated_image_data objective5 high_res  )  
(communicated_image_data objective1 colour  )  
(communicated_image_data objective1 low_res  )  
	  )  
  )  
  )  
