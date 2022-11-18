def numbers_to_strings(argument):
    switcher = {"Alandur Bus Depot, Chennai - CPCB    Chennai, Tamil Nadu":1,
                "Bandra, Mumbai - MPCB":2,
                "Belur Math, Howrah - WBPCB    Howrah, West Bengal":3,
                "BWSSB Kadabesanahalli, Bengaluru - CPCB    Bengaluru, Karnataka":4,
                "Chhatrapati Shivaji Intl. Airport (T2), Mumbai - MPCB":5,
                "Deshpande Nagar, Hubballi - KSPCB Hubbali Karnataka":6,
                "Dr. Karni Singh Shooting Range, Delhi - DPCC Delhi":7,
                "Fort William, Kolkata - WBPCB Kolkata West bengal":8,
                "Golden Temple, Amritsar - PPCB Amritsar Punjab":9,
                "GVM Corporation, Visakhapatnam - APPCB, Visakhapatnam, Andhra Pradesh":10,
                "Haji Colony, Raichur - KSPCB":11,
                "Knowledge Park - III, Greater Noida - UPPCB Greater Noida Uttar Pradesh":12,
                "Mandir Marg, Delhi - DPCC Delhi":13,
                "Maninagar, Ahmedabad - GPCB Ahmedabad":14,
                "MIDC Khutala, Chandrapur - MPCB":15,
                "Muradpur, Patna - BSPCB Patna Bihar":16,
                "NSIT Dwarka, Delhi - CPCB":17,
                "Railway Colony, Guwahati - APCB Guwahati Assam":18,
                "Sector- 16A, Faridabad - HSPCB Faridabad Haryana":19,
                "T T Nagar, Bhopal - MPPCB Bhopal Madhya Pradesh":20,
                "Talcher Coalfields,Talcher - OSPCB Talcher Odisha":21,
                "Talkatora District Industries Center, Lucknow - CPCB Lucknow Uttar Pradesh":22,
                "Tamaka Ind. Area, Kolar - KSPCB":23,
                "Ward-32 Bapupara, Siliguri - WBPCB":24,
              
                "Arya Nagar, Bahadurgarh - HSPCB":25,
                "Chhoti Gwaltoli, Indore - MPPCB":26,
                "Dwarka-Sector 8, Delhi - DPCC":27,
                "GIDC, Ankleshwar - GPCB":28,
                "GM Office, Brajrajnagar - OSPCB":29,
                "Kalal Majra, Khanna - PPCB":30,
                "Lodhi Road, Delhi - IITM":31,
                "Mangala, Bilaspur - NTPC":32,
                "MIDC Khutala, Chandrapur - MPCB":33,
                "More Chowk Waluj, Aurangabad - MPCB":34,
                "Muradpur, Patna - BSPCB Patna Bihar":35,
                "Plammoodu, Thiruvananthapuram - Kerala PCB":36,
                "Punjabi Bagh, Delhi - DPCC":37,
                "Sector-1, Noida - UPPCB":38,
                "Sector-10, Gandhinagar - GPCB":39,
                "Sikulpuikawn, Aizawl - Mizoram PCB":40,
                "Sirifort, Delhi - CPCB":41,
                "Udyogamandal, Eloor - Kerala PCB":42,
                'Rohini, Delhi - DPCC': 43,
                'IGI Airport (T3), Delhi - IMD': 44,
                'Jadavpur, Kolkata - WBPCB': 45,
                'Bidhannagar, Kolkata - WBPCB': 46,
                'Victoria, Kolkata - WBPCB': 47,
                
                'Rabindra Sarobar, Kolkata - WBPCB': 48,
                'Rabindra Bharati University, Kolkata - WBPCB': 49,
                'Ballygunge, Kolkata - WBPCB': 50,
                'Pusa, Delhi - IMD':51,
                'Pusa, Delhi - DPCC':52,
                'Model Town, Patiala - PPCB':53,
                

               
               
               
               }

    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(argument, "nothing")
