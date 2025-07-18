import pandas as pd
from io import StringIO

# Paste your data into 'data' (as a string)
data = """
District	State	Latitude	Longitude
Adilabad	ANDHRA PRADESH	19.663259	78.555315
Agra	UTTAR PRADESH	27.17568	78.008109
Ahmadabad	GUJARAT	23.026157	72.589687
Ahmadnagar	MAHARASHTRA	19.093412	74.746855
Aizawl	MIZORAM	23.748659	92.728016
Ajmer	RAJASTHAN	26.460578	74.641756
Akola	MAHARASHTRA	20.710576	77.00373
Alappuzha	KERALA	9.501632	76.329606
Aligarh	UTTAR PRADESH	27.875204	78.068216
Allahabad	UTTAR PRADESH	25.45399	81.851869
Almora	UTTARANCHAL	29.603844	79.665557
Alwar	RAJASTHAN	27.566581	76.610602
Ambala	HARYANA	30.376076	76.78821
Ambedkar Nagar *	UTTAR PRADESH	26.413411	82.54027
Amravati	MAHARASHTRA	20.937346	77.760249
Amreli	GUJARAT	21.598002	71.216081
Amritsar	PUNJAB	31.623088	74.87248
Anand  *	GUJARAT	22.566883	72.953775
Anantapur	ANDHRA PRADESH	14.679395	77.598252
Anantnag	JAMMU & KASHMIR	33.738528	75.16328
Andamans	ANDAMAN & NICOBAR	11.660569	92.741136
Anjaw	ARUNACHAL PRADESH	27.894204	96.790213
Anugul  *	ORISSA	20.836481	85.099192
Anuppur	MADHYA PRADESH	23.097789	81.701139
Araria	BIHAR	26.137794	87.464469
Ashok Nagar	MADHYA PRADESH	24.568718	77.728572
Auraiya *	UTTAR PRADESH	26.460045	79.519467
Aurangabad	BIHAR	24.749745	84.379225
Aurangabad	MAHARASHTRA	19.885543	75.333441
Azamgarh	UTTAR PRADESH	26.053641	83.181213
Bagalkot *	KARNATAKA	16.202963	75.707787
Bageshwar	UTTARANCHAL	29.842812	79.770905
Baghpat *	UTTAR PRADESH	28.934887	77.226645
Bahraich	UTTAR PRADESH	27.577746	81.598143
Balaghat	MADHYA PRADESH	21.815447	80.1932
Balangir	ORISSA	20.705399	83.496116
Baleshwar	ORISSA	21.492432	86.922744
Ballia	UTTAR PRADESH	25.760427	84.155791
Balrampur *	UTTAR PRADESH	27.424362	82.195912
Banas Kantha	GUJARAT	24.185024	72.444088
Banda	UTTAR PRADESH	25.467372	80.325071
Bangalore	KARNATAKA	12.97708	77.596173
Bangalore	KARNATAKA	12.97708	77.596173
Banka *	BIHAR	24.880617	86.919712
Bankura	WEST BENGAL	23.249965	87.061434
Banswara	RAJASTHAN	23.545683	74.448134
Barabanki	UTTAR PRADESH	26.931977	81.203728
Baramula	JAMMU & KASHMIR	34.200628	74.328035
Baran *	RAJASTHAN	25.113409	76.513669
Barddhaman	WEST BENGAL	23.262279	87.856827
Bareilly	UTTAR PRADESH	28.361856	79.419697
Bargarh  *	ORISSA	21.339228	83.63098
Barmer	RAJASTHAN	25.743971	71.393059
Barpeta	ASSAM	26.318438	91.012313
Barwani *	MADHYA PRADESH	22.02929	74.891275
Baster	CHHATTISGARH	19.086747	82.039276
Basti	UTTAR PRADESH	26.801568	82.758574
Bathinda	PUNJAB	30.293282	74.951926
Baudh  *	ORISSA	20.832374	83.922946
Baudh  *	ORISSA	20.826237	84.307596
Begusarai	BIHAR	25.409515	86.135757
Belgaum	KARNATAKA	15.858948	74.509438
Bellary	KARNATAKA	15.143301	76.923557
Betul	MADHYA PRADESH	21.903513	77.902064
Bhadrak  *	ORISSA	21.068425	86.503508
Bhagalpur	BIHAR	25.239305	86.974522
Bhandara	MAHARASHTRA	21.169245	79.657152
Bharatpur	RAJASTHAN	27.213921	77.500799
Bharuch	GUJARAT	21.69417	72.978556
Bhavnagar	GUJARAT	21.77414	72.139722
Bhilwara	RAJASTHAN	25.347483	74.637973
Bhind	MADHYA PRADESH	26.564114	78.789336
Bhiwani	HARYANA	28.791052	76.143875
Bhojpur	BIHAR	25.565465	84.677244
Bhopal	MADHYA PRADESH	23.266323	77.414303
Bid	MAHARASHTRA	18.987824	75.763809
Bidar	KARNATAKA	17.915869	77.531757
Bijapur	KARNATAKA	16.823754	75.719178
Bijnor	UTTAR PRADESH	29.379583	78.13407
Bikaner	RAJASTHAN	28.016543	73.317199
Bilaspur	HIMACHAL PRADESH	31.323902	76.761527
Bilaspur	CHHATTISGARH	22.074605	82.176189
Birbhum	WEST BENGAL	23.908735	87.534251
Bishnupur	MANIPUR	24.632371	93.764667
Bokaro *	JHARKHAND	23.640657	86.162947
Bongaigaon	ASSAM	26.502443	90.564968
Budaun	UTTAR PRADESH	28.034404	79.124138
Bulandshahr	UTTAR PRADESH	28.400237	77.861025
Buldana	MAHARASHTRA	20.532223	76.181689
Bundi	RAJASTHAN	25.442985	75.643423
Burhanpur	MADHYA PRADESH	21.33186	76.20459
Buxar *	BIHAR	25.571102	83.98059
Cachar	ASSAM	24.820025	92.795038
Chamba	HIMACHAL PRADESH	32.558843	76.126097
Chamoli	UTTARANCHAL	30.401381	79.331112
Champawat	UTTARANCHAL	29.333337	80.103959
Champhai *	MIZORAM	23.489023	93.345186
Chamrajnagar*	KARNATAKA	11.936475	76.939171
Chandauli *	UTTAR PRADESH	25.258531	83.270958
Chandel	MANIPUR	24.320947	93.989857
Chandigarh	CHANDIGARH	30.731928	76.785486
Chandrapur	MAHARASHTRA	19.951685	79.295823
Changlang	ARUNACHAL PRADESH	27.087745	95.731123
Chatra *	JHARKHAND	24.208676	84.866295
Chennai	TAMIL NADU	13.074737	80.267689
Chhatarpur	MADHYA PRADESH	24.915425	79.592243
Chhindwara	MADHYA PRADESH	22.057572	78.940098
Chikmagalur	KARNATAKA	13.318348	75.772746
Chitradurga	KARNATAKA	14.227245	76.402839
Chitrakoot *	UTTAR PRADESH	25.210734	80.914156
Chittaurgarh	RAJASTHAN	24.876434	74.619443
Chittoor	ANDHRA PRADESH	13.215319	79.100032
Churachandpur	MANIPUR	24.334438	93.658102
Churu	RAJASTHAN	28.300078	74.966601
Coimbatore	TAMIL NADU	10.994743	76.96688
Cuddalore	TAMIL NADU	11.75553	79.762325
Cuddapah	ANDHRA PRADESH	14.482391	78.82537
Cuttack	ORISSA	20.478116	85.85389
Dadra & Nagar Haveli	DADRA & NAGAR HAVE	20.284446	72.998942
Dakshin Dinajpur *	WEST BENGAL	25.230003	88.789755
Dakshina Kannada	KARNATAKA	12.863889	74.841219
Daman	DAMAN & DIU	20.424388	72.846682
Damoh	MADHYA PRADESH	23.824248	79.455215
Dantewada*	CHHATTISGARH	18.87715	81.367201
Darbhanga	BIHAR	26.164221	85.910612
Darjiling	WEST BENGAL	27.041527	88.272768
Darrang	ASSAM	26.441811	92.033565
Datia	MADHYA PRADESH	25.673026	78.458158
Dausa *	RAJASTHAN	26.899411	76.334441
Davangere*	KARNATAKA	14.492934	75.936375
Debagarh  *	ORISSA	21.546245	84.744026
Dehradun	UTTARANCHAL	30.325264	78.041576
Deoghar	JHARKHAND	24.481265	86.700615
Deoria	UTTAR PRADESH	26.500556	83.783389
Dewas	MADHYA PRADESH	22.962736	76.071156
Dhalai  *	TRIPURA	23.938769	91.868389
Dhamtari *	CHHATTISGARH	20.703812	81.567596
Dhanbad	JHARKHAND	23.797727	86.436225
Dhar	MADHYA PRADESH	22.598554	75.314536
Dharmapuri	TAMIL NADU	12.134803	78.161203
Dharwad	KARNATAKA	15.452454	75.012073
Dhaulpur	RAJASTHAN	26.693948	77.894554
Dhemaji	ASSAM	27.4844	94.594933
Dhenkanal	ORISSA	20.654734	85.588016
Dhubri	ASSAM	26.019042	89.991086
Dhule	MAHARASHTRA	20.90441	74.781243
Dibang Valley	ARUNACHAL PRADESH	28.850861	95.871559
Dibrugarh	ASSAM	27.480193	94.912419
Dimapur *	NAGALAND	25.91789	93.746839
Dindigul	TAMIL NADU	10.361936	77.968908
Dindori *	MADHYA PRADESH	22.939702	81.083584
Diu	DAMAN & DIU	20.713309	70.979548
Dohad  *	GUJARAT	22.823003	74.263925
Dumka	JHARKHAND	24.271014	87.249367
Dungarpur	RAJASTHAN	23.837104	73.716702
Durg	CHHATTISGARH	21.188278	81.275855
East	SIKKIM	27.328923	88.616469
East Garo Hills	MEGHALAYA	25.528369	90.593784
East Godavari	ANDHRA PRADESH	16.969397	82.236435
East Kameng	ARUNACHAL PRADESH	27.333113	93.063248
East Khasi Hills	MEGHALAYA	25.588025	91.887356
East Nimar	MADHYA PRADESH	21.827574	76.356018
East Siang	ARUNACHAL PRADESH	28.065355	95.333325
Ernakulam	KERALA	9.956764	76.292401
Erode	TAMIL NADU	11.334348	77.72772
Etah	UTTAR PRADESH	27.55673	78.657582
Etawah	UTTAR PRADESH	26.77697	79.025561
Faizabad	UTTAR PRADESH	26.781125	82.149876
Faridabad	HARYANA	28.427902	77.329409
Faridkot	PUNJAB	30.67333	74.758547
Farrukhabad	UTTAR PRADESH	27.367541	79.635106
Fatehabad *	HARYANA	29.516385	75.4548
Fatehgarh Sahib *	PUNJAB	30.647528	76.406922
Fatehpur	UTTAR PRADESH	25.927961	80.817369
Firozabad	UTTAR PRADESH	27.142217	78.398303
Firozpur	PUNJAB	30.939516	74.619239
Gadag *	KARNATAKA	15.441432	75.646857
Gadchiroli	MAHARASHTRA	20.184794	80.007887
Gajapati  *	ORISSA	18.776646	84.080324
Gandhinagar	GUJARAT	23.235737	72.671374
Ganganagar	RAJASTHAN	29.928315	73.867201
Ganjam	ORISSA	19.350441	84.985993
Garhwa *	JHARKHAND	24.17351	83.81231
Garhwal	UTTARANCHAL	30.152136	78.780959
Gautam Buddha Nagar *	UTTAR PRADESH	28.567013	77.327519
Gaya	BIHAR	24.79151	85.004475
Ghaziabad	UTTAR PRADESH	28.660255	77.445653
Ghazipur	UTTAR PRADESH	25.586118	83.581496
Giridih	JHARKHAND	24.189967	86.313267
Goalpara	ASSAM	26.176465	90.631164
Godda	JHARKHAND	24.829078	87.215924
Golaghat	ASSAM	26.509522	93.974001
Gonda	UTTAR PRADESH	27.133796	81.962471
Gondiya *	MAHARASHTRA	21.448734	80.1972
Gopalganj	BIHAR	26.465323	84.444294
Gorakhpur	UTTAR PRADESH	26.759828	83.370935
Gulbarga	KARNATAKA	17.334962	76.834784
Gumla	JHARKHAND	23.026635	84.534374
Guna	MADHYA PRADESH	24.644351	77.313136
Guntur	ANDHRA PRADESH	16.297356	80.447394
Gurdaspur	PUNJAB	32.045131	75.408744
Gurgaon	HARYANA	28.466248	77.028569
Gwalior	MADHYA PRADESH	26.222524	78.168463
Hailakandi	ASSAM	24.709416	92.568191
Hamirpur	HIMACHAL PRADESH	31.672705	76.521404
Hamirpur	UTTAR PRADESH	25.959941	80.117055
Hanumangarh *	RAJASTHAN	29.577336	74.320427
Haora	WEST BENGAL	22.567906	88.327811
Harda *	MADHYA PRADESH	22.336719	77.085484
Hardoi	UTTAR PRADESH	27.395551	80.127149
Hardwar	UTTARANCHAL	29.919595	78.162848
Hassan	KARNATAKA	13.008913	76.098149
Hathras *	UTTAR PRADESH	27.585241	78.05918
Haveri *	KARNATAKA	14.810215	75.407562
Hazaribag	JHARKHAND	23.988567	85.36671
Hingoli *	MAHARASHTRA	19.713154	77.153409
Hisar	HARYANA	29.151765	75.725027
Hoshangabad	MADHYA PRADESH	22.740101	77.713729
Hoshiarpur	PUNJAB	31.535053	75.914418
Hugli	WEST BENGAL	22.900631	88.396631
Hyderabad	ANDHRA PRADESH	17.399667	78.488244
Hyderabad	ANDHRA PRADESH	17.399667	78.488244
Idukki	KERALA	9.900515	77.176271
Imphal East *	MANIPUR	24.811571	93.950799
Indore	MADHYA PRADESH	22.716881	75.867271
Jabalpur	MADHYA PRADESH	23.172246	79.937619
Jagatsinghapur  *	ORISSA	20.26385	86.166024
Jaintia Hills	MEGHALAYA	25.438113	92.198261
Jaipur	RAJASTHAN	26.914736	75.810664
Jaisalmer	RAJASTHAN	26.911481	70.91459
Jajapur  *	ORISSA	20.844687	86.32523
Jalandhar	PUNJAB	31.339673	75.581698
Jalaun	UTTAR PRADESH	25.989945	79.454191
Jalgaon	MAHARASHTRA	21.009559	75.570044
Jalna	MAHARASHTRA	19.848844	75.901627
Jalor	RAJASTHAN	25.342919	72.620614
Jalpaiguri	WEST BENGAL	26.527845	88.719039
Jammu	JAMMU & KASHMIR	32.727401	74.8456
Jamnagar	GUJARAT	22.471076	70.07265
Jamtara	JHARKHAND	23.959798	86.788385
Jamui *	BIHAR	24.925934	86.216344
Janjgir – Champa*	CHHATTISGARH	22.003783	82.594618
Jashpur *	CHHATTISGARH	22.892329	84.158393
Jaunpur	UTTAR PRADESH	25.748744	82.687741
Jehanabad	BIHAR	25.212198	84.982009
Jhabua	MADHYA PRADESH	22.769906	74.599553
Jhajjar *	HARYANA	28.601349	76.6536
Jhalawar	RAJASTHAN	24.592312	76.165807
Jhansi	UTTAR PRADESH	25.462975	78.57546
Jharsuguda  *	ORISSA	21.851989	84.025951
Jhunjhunun	RAJASTHAN	28.129504	75.400108
Jind	HARYANA	29.318821	76.313347
Jodhpur	RAJASTHAN	26.279624	73.022778
Jorhat	ASSAM	26.754666	94.218519
Junagadh	GUJARAT	21.522705	70.461296
Jyotiba Phule Nagar *	UTTAR PRADESH	28.906416	78.462509
Kachchh	GUJARAT	23.251213	69.666108
Kaimur (Bhabua) *	BIHAR	25.040295	83.602718
Kaithal	HARYANA	29.804185	76.399321
Kalahandi	ORISSA	19.910373	83.176494
Kamrup	ASSAM	26.181061	91.751916
Kancheepuram	TAMIL NADU	12.834822	79.715697
Kandhamal	ORISSA	20.467657	84.240574
Kangra	HIMACHAL PRADESH	32.217751	76.31406
Kanker *	CHHATTISGARH	20.275167	81.50583
Kannauj *	UTTAR PRADESH	27.056124	79.926694
Kanniyakumari	TAMIL NADU	8.175865	77.440953
Kannur	KERALA	11.868687	75.36639
Kanpur Dehat	UTTAR PRADESH	26.375967	79.955267
Kanpur Nagar	UTTAR PRADESH	26.461855	80.344194
Kapurthala	PUNJAB	31.379585	75.385678
Karaikal	PONDICHERRY	10.917964	79.837646
Karauli *	RAJASTHAN	26.4987	77.022184
Karbi Anglong	ASSAM	25.838215	93.446934
Karimganj	ASSAM	24.871588	92.353828
Karimnagar	ANDHRA PRADESH	18.431912	79.144791
Karnal	HARYANA	29.692495	76.985142
Karur  *	TAMIL NADU	10.948948	78.086832
Kasaragod	KERALA	12.498305	74.990213
Kathua	JAMMU & KASHMIR	32.359369	75.516357
Katihar	BIHAR	25.537374	87.583497
Katni *	MADHYA PRADESH	23.841092	80.397878
Kaushambi *	UTTAR PRADESH	25.524545	81.383437
Kawardha *	CHHATTISGARH	22.006266	81.259515
Kendrapara *	ORISSA	20.508399	86.417262
Kendujhar	ORISSA	21.644926	85.583459
Khagaria	BIHAR	25.508751	86.472735
Khammam	ANDHRA PRADESH	17.245344	80.140567
Kheda	GUJARAT	22.747316	72.695273
Kheri	UTTAR PRADESH	27.947796	80.788432
Khordha  *	ORISSA	20.187781	85.622131
Kinnaur	HIMACHAL PRADESH	31.546954	78.26285
Kishanganj	BIHAR	26.112966	87.9283
Koch Bihar	WEST BENGAL	26.328292	89.453617
Kodagu	KARNATAKA	12.422433	75.744027
Kodarma *	JHARKHAND	24.463	85.587047
Kohima	NAGALAND	25.684924	94.118903
Kokrajhar	ASSAM	26.40281	90.273819
Kolar	KARNATAKA	13.135759	78.136263
Kolasib *	MIZORAM	24.252182	92.690303
Kolhapur	MAHARASHTRA	16.694394	74.22406
Kolkata	WEST BENGAL	22.548783	88.39894
Kollam	KERALA	8.888392	76.609021
Koppal *	KARNATAKA	15.362997	76.167916
Koraput	ORISSA	18.80694	82.719909
Korba *	CHHATTISGARH	22.337193	82.715651
Koriya *	CHHATTISGARH	23.244843	82.570516
Kota	RAJASTHAN	25.179993	75.846204
Kottayam	KERALA	9.595602	76.521426
Kozhikode	KERALA	11.239895	75.795215
Krishna	ANDHRA PRADESH	16.189204	81.136184
Krishnagiri	TAMIL NADU	12.533802	78.228528
Kullu	HIMACHAL PRADESH	31.960573	77.107897
Kurnool	ANDHRA PRADESH	15.834985	78.041533
Kurukshetra	HARYANA	29.962444	76.838151
Kurung Kumey	ARUNACHAL PRADESH	27.861258	93.499644
Kushinagar *	UTTAR PRADESH	26.907172	83.985134
Lahul & Spiti	HIMACHAL PRADESH	32.574709	77.040806
Lakhimpur	ASSAM	27.236148	94.105136
Lakhisarai *	BIHAR	25.176411	86.090783
Lakshdweep	LAKSHADWEEP	10.568609	72.640306
Lalitpur	UTTAR PRADESH	24.691585	78.418609
Latehar	JHARKHAND	23.75162	84.509376
Latur	MAHARASHTRA	18.401122	76.576955
Leh(Ladakh)	JAMMU & KASHMIR	34.138736	77.565158
Lohardaga	JHARKHAND	23.432486	84.681568
Lohit	ARUNACHAL PRADESH	27.925439	96.166869
Lower Dibang Valley	ARUNACHAL PRADESH	28.1375	95.798781
Lower Subansiri	ARUNACHAL PRADESH	27.5556	93.812343
Lucknow	UTTAR PRADESH	26.83323	80.943614
Ludhiana	PUNJAB	30.908679	75.851626
Lunglei	MIZORAM	22.888359	92.746609
Madhepura	BIHAR	25.921099	86.792579
Madhubani	BIHAR	26.356596	86.070431
Madurai	TAMIL NADU	9.924937	78.129356
Maharajganj	UTTAR PRADESH	27.146858	83.567801
Mahasamund *	CHHATTISGARH	21.09393	82.111104
Mahbubnagar	ANDHRA PRADESH	16.744426	77.991612
Mahendragarh	HARYANA	28.045836	76.11006
Mahesana	GUJARAT	23.60274	72.385689
Mahoba *	UTTAR PRADESH	25.286105	79.880627
Mainpuri	UTTAR PRADESH	27.229325	79.049369
Malappuram	KERALA	11.043786	76.085683
Maldah	WEST BENGAL	25.010231	88.147599
Malkangiri  *	ORISSA	18.357914	81.897509
Mamit *	MIZORAM	23.942233	92.499553
Mandi	HIMACHAL PRADESH	31.711956	76.932031
Mandla	MADHYA PRADESH	22.605889	80.370917
Mandsaur	MADHYA PRADESH	24.063675	75.074883
Mandya	KARNATAKA	12.517368	76.898666
Mansa *	PUNJAB	29.986894	75.390143
Marigaon	ASSAM	26.255106	92.337553
Mathura	UTTAR PRADESH	27.494256	77.684411
Mau	UTTAR PRADESH	25.947961	83.561419
Mayurbhanj	ORISSA	21.944929	86.725858
Medak	ANDHRA PRADESH	17.625811	78.082342
Meerut	UTTAR PRADESH	28.986554	77.70386
Mirzapur	UTTAR PRADESH	25.143896	82.562668
Moga *	PUNJAB	30.801361	75.162775
Mokokchung	NAGALAND	26.321208	94.519572
Mon	NAGALAND	26.723923	95.031768
Moradabad	UTTAR PRADESH	28.832848	78.780652
Morena	MADHYA PRADESH	26.500863	78.001752
Muktsar *	PUNJAB	30.463978	74.517016
Mumbai	MAHARASHTRA	18.987074	72.830007
Mumbai (Suburban) *	MAHARASHTRA	19.054135	72.832678
Munger	BIHAR	25.37403	86.47675
Murshidabad	WEST BENGAL	24.100513	88.278789
Muzaffarnagar	UTTAR PRADESH	29.471716	77.700412
Muzaffarpur	BIHAR	26.117382	85.406908
Mysore	KARNATAKA	12.309442	76.654533
Nabarangapur  *	ORISSA	19.224792	82.557829
Nadia	WEST BENGAL	23.418592	88.504458
Nagaon	ASSAM	26.355771	92.686525
Nagapattinam  *	TAMIL NADU	10.770587	79.834871
Nagaur	RAJASTHAN	27.200302	73.736974
Nagpur	MAHARASHTRA	21.148204	79.096814
Nainital	UTTARANCHAL	29.380565	79.470524
Nalanda	BIHAR	25.194764	85.521417
Nalbari	ASSAM	26.444776	91.445234
Nalgonda	ANDHRA PRADESH	17.061325	79.267503
Namakkal   *	TAMIL NADU	11.225821	78.171836
Nanded	MAHARASHTRA	19.159314	77.313188
Nandurbar *	MAHARASHTRA	21.36675	74.244736
Narmada  *	GUJARAT	21.875823	73.499823
Narsimhapur	MADHYA PRADESH	22.948386	79.193312
Nashik	MAHARASHTRA	20.006006	73.795878
Navsari  *	GUJARAT	20.948755	72.925226
Nawada	BIHAR	24.887955	85.543198
Nawanshahr *	PUNJAB	31.120012	76.130554
Nayagarh  *	ORISSA	20.120189	85.098925
Neemuch *	MADHYA PRADESH	24.473691	74.876342
Nellore	ANDHRA PRADESH	14.449206	79.983616
Nizamabad	ANDHRA PRADESH	18.654235	78.09389
North	SIKKIM	27.50395	88.536203
North Cachar Hills	ASSAM	25.167627	93.015884
North Goa	GOA	15.480081	73.822329
North Tripura	TRIPURA	24.342116	92.017914
North Twenty Four Pargana	WEST BENGAL	22.724797	88.507529
Nuapada  *	ORISSA	20.819327	82.555776
Osmanabad	MAHARASHTRA	18.181663	76.041686
Pachim Sionghum	JHARKHAND	22.554553	85.808737
Pakaur *	JHARKHAND	24.635842	87.834711
Palakkad	KERALA	10.772089	76.658319
Palamu	JHARKHAND	24.040242	84.069328
Pali	RAJASTHAN	25.777043	73.322215
Panch Mahals	GUJARAT	22.772915	73.60953
Panchkula *	HARYANA	30.722619	76.880191
Panipat	HARYANA	29.387951	76.968552
Panna	MADHYA PRADESH	24.719464	80.189266
Papum Pare *	ARUNACHAL PRADESH	27.101465	93.597901
Parbhani	MAHARASHTRA	19.268358	76.777025
Paschim Medinapur	WEST BENGAL	22.42833	87.323882
Pashchim Champaran	BIHAR	26.804014	84.510335
Patan  *	GUJARAT	23.845103	72.111466
Pathanamthitta	KERALA	9.294782	76.75528
Patiala	PUNJAB	30.317367	76.407038
Patna	BIHAR	25.603125	85.119195
Perambalur	TAMIL NADU	11.243109	78.866417
Phek	NAGALAND	25.701797	94.465739
Pilibhit	UTTAR PRADESH	28.634994	79.812128
Pithoragarh	UTTARANCHAL	29.583696	80.203698
Pondicherry	PONDICHERRY	11.935363	79.83229
Porbandar	GUJARAT	21.636581	69.59674
Prakasam	ANDHRA PRADESH	15.514451	80.048738
Pratapgarh	UTTAR PRADESH	25.93741	81.995137
Pudukkottai	TAMIL NADU	10.383944	78.81216
Punch	JAMMU & KASHMIR	33.773791	74.081247
Pune	MAHARASHTRA	18.525994	73.862602
Purba Champaran	BIHAR	26.653574	84.925161
Purba Medinapur	WEST BENGAL	22.301044	87.919817
Purbi Singhbhum	JHARKHAND	22.799522	86.197389
Puri	ORISSA	19.79549	85.838807
Purnia	BIHAR	25.777226	87.47066
Puruliya	WEST BENGAL	23.332193	86.366718
Rae Bareli	UTTAR PRADESH	26.231689	81.230631
Raichur	KARNATAKA	16.207752	77.358779
Raigarh	CHHATTISGARH	21.908949	83.395958
Raigarh	MAHARASHTRA	18.646539	72.875994
Raipur	CHHATTISGARH	21.227374	81.629069
Raisen	MADHYA PRADESH	23.33011	77.780588
Rajgarh	MADHYA PRADESH	24.005868	76.739744
Rajkot	GUJARAT	22.295207	70.805355
Rajnandgaon	CHHATTISGARH	21.089426	81.034625
Rajsamand *	RAJASTHAN	25.075336	73.860393
Ramanathapuram	TAMIL NADU	9.363516	78.840969
Rampur	UTTAR PRADESH	28.791807	79.029148
Ranchi	JHARKHAND	23.363068	85.340321
Ratlam	MADHYA PRADESH	23.327034	75.040755
Ratnagiri	MAHARASHTRA	16.990597	73.297537
Rayagada  *	ORISSA	19.165286	83.412105
Rewa	MADHYA PRADESH	24.540725	81.288305
Rewari	HARYANA	28.198138	76.615433
Ri Bhoi  *	MEGHALAYA	25.915944	91.88132
Rohtak	HARYANA	28.888214	76.587935
Rohtas	BIHAR	24.92088	84.039698
Rudraprayag *	UTTARANCHAL	30.29541	78.986665
Rupnagar	PUNJAB	30.964466	76.526375
Sabar Kantha	GUJARAT	23.605115	72.96492
Sagar	MADHYA PRADESH	23.837188	78.749867
Saharanpur	UTTAR PRADESH	29.965049	77.553476
Saharsa	BIHAR	25.872235	86.59889
Sahibganj	JHARKHAND	25.244524	87.632966
Saiha *	MIZORAM	22.513447	92.979389
Salem	TAMIL NADU	11.65821	78.152968
Samastipur	BIHAR	25.846512	85.779185
Sambalpur	ORISSA	21.466623	83.986047
Sangli	MAHARASHTRA	16.860757	74.57878
Sangrur	PUNJAB	30.241479	75.841924
Sant Kabir Nagar *	UTTAR PRADESH	26.778133	83.086966
Sant Ravidas Nagar *	UTTAR PRADESH	25.335702	82.46387
Saraikela	JHARKHAND	22.715002	85.939556
Saran	BIHAR	25.777293	84.751385
Satara	MAHARASHTRA	17.690393	74.010744
Satna	MADHYA PRADESH	24.566488	80.833433
Sawai Madhopur	RAJASTHAN	25.987844	76.381194
Sehore	MADHYA PRADESH	23.206208	77.085006
Senapati	MANIPUR	25.302888	94.048471
Seoni	MADHYA PRADESH	22.088143	79.548337
Serchhip *	MIZORAM	23.3256	92.864991
Shahdol	MADHYA PRADESH	23.294345	81.360684
Shahjahanpur	UTTAR PRADESH	27.871092	79.908609
Shajapur	MADHYA PRADESH	23.423091	76.280682
Sheikhpura *	BIHAR	25.147495	85.839471
Sheohar *	BIHAR	26.514445	85.29636
Sheopur *	MADHYA PRADESH	25.676035	76.698332
Shimla	HIMACHAL PRADESH	31.10003	77.171181
Shimoga	KARNATAKA	13.930893	75.576068
Shivpuri	MADHYA PRADESH	25.42602	77.653283
Shrawasti *	UTTAR PRADESH	27.700545	81.931928
Sibsagar	ASSAM	26.984297	94.639508
Siddharthnagar	UTTAR PRADESH	27.246253	83.066141
Sidhi	MADHYA PRADESH	24.409558	81.883792
Sikar	RAJASTHAN	27.610617	75.147048
Simdega	JHARKHAND	22.615172	84.502538
Sindhudurg	MAHARASHTRA	16.107985	73.714977
Sirmaur	HIMACHAL PRADESH	30.525617	77.230732
Sirohi	RAJASTHAN	24.89138	72.857774
Sirsa	HARYANA	29.531177	75.026343
Sitamarhi	BIHAR	26.59391	85.496766
Sitapur	UTTAR PRADESH	27.563585	80.686343
Sivaganga	TAMIL NADU	9.860311	78.481581
Siwan	BIHAR	26.22132	84.361494
Solan	HIMACHAL PRADESH	30.910522	77.108405
Solapur	MAHARASHTRA	17.672099	75.907906
Sonbhadra	UTTAR PRADESH	24.687697	83.069029
Sonipat	HARYANA	28.979449	77.024728
Sonitpur	ASSAM	26.623221	92.791733
South	SIKKIM	27.163151	88.359601
South  Twenty Four Pargan	WEST BENGAL	22.484754	88.265534
South Garo Hills *	MEGHALAYA	25.200104	90.645557
South Goa	GOA	15.304936	73.959411
South Tripura	TRIPURA	23.53045	91.485363
Srikakulam	ANDHRA PRADESH	18.296866	83.891833
Srinagar	JAMMU & KASHMIR	34.083627	74.810746
Sultanpur	UTTAR PRADESH	26.262349	82.073784
Sundargarh	ORISSA	22.128217	84.048498
Supaul *	BIHAR	26.246247	86.644513
Surat	GUJARAT	21.205128	72.847119
Surendranagar	GUJARAT	22.732978	71.614645
Surguja	CHHATTISGARH	23.118939	83.207362
Tamenglong	MANIPUR	24.996325	93.502375
Tawang	ARUNACHAL PRADESH	27.587899	91.885444
Tehri Garhwal	UTTARANCHAL	30.376102	78.498598
Thane	MAHARASHTRA	19.205931	72.971198
Thanjavur	TAMIL NADU	10.785111	79.138403
The Dangs	GUJARAT	20.756817	73.689483
The Nilgiris	TAMIL NADU	11.415521	76.705867
Theni	TAMIL NADU	9.999588	77.464364
Thiruvallur	TAMIL NADU	13.153773	79.915219
Thiruvananthapuram	KERALA	8.490191	76.917805
Thiruvarur	TAMIL NADU	10.780886	79.626455
Thoothukkudi	TAMIL NADU	8.810166	78.148882
Thoubal	MANIPUR	24.637889	94.006052
Thrissur	KERALA	10.522671	76.21865
Tikamgarh	MADHYA PRADESH	24.743252	78.831962
Tinsukia	ASSAM	27.49208	95.370027
Tirap	ARUNACHAL PRADESH	26.991189	95.50663
Tiruchirappalli	TAMIL NADU	10.82225	78.681043
Tirunelveli	TAMIL NADU	8.730059	77.692464
Tiruvannamalai	TAMIL NADU	12.233386	79.07432
Tonk	RAJASTHAN	26.171361	75.788097
Tuensang	NAGALAND	26.229854	94.814512
Tumkur	KARNATAKA	13.353655	77.096527
Udaipur	RAJASTHAN	24.585424	73.686924
Udham Singh Nagar *	UTTARANCHAL	28.966203	79.396914
Udhampur	JAMMU & KASHMIR	32.91258	75.108491
Udupi *	KARNATAKA	13.359567	74.759237
Ujjain	MADHYA PRADESH	23.185696	75.779601
Ukhrul	MANIPUR	25.091234	94.363891
Umaria *	MADHYA PRADESH	23.525654	80.837774
Una	HIMACHAL PRADESH	31.46426	76.268458
Unnao	UTTAR PRADESH	26.545632	80.489814
Upper Siang *	ARUNACHAL PRADESH	28.613345	95.066152
Upper Subansiri	ARUNACHAL PRADESH	28.029687	94.216858
Uttar Dinajpur	WEST BENGAL	25.609131	88.125952
Uttara Kannada	KARNATAKA	14.804209	74.131214
Uttarkashi	UTTARANCHAL	30.715986	78.430542
Vadodara	GUJARAT	22.287726	73.206027
Vaishali	BIHAR	25.676599	85.219298
Valsad	GUJARAT	20.631227	72.933378
Varanasi	UTTAR PRADESH	25.325043	82.975165
Vellore	TAMIL NADU	12.909641	79.139241
Vidisha	MADHYA PRADESH	23.531456	77.812138
Viluppuram	TAMIL NADU	11.936979	79.487333
Virudhunagar	TAMIL NADU	9.594003	77.952743
Visakhapatnam	ANDHRA PRADESH	17.724253	83.305865
Vizianagaram	ANDHRA PRADESH	18.124612	83.406912
Warangal	ANDHRA PRADESH	18.030289	79.57543
Wardha	MAHARASHTRA	20.735221	78.604456
Washim *	MAHARASHTRA	20.108935	77.142117
Wayanad	KERALA	11.606117	76.088347
West	SIKKIM	27.290085	88.244703
West Garo Hills	MEGHALAYA	25.505214	90.280827
West Godavari	ANDHRA PRADESH	16.719836	81.100761
West Kameng	ARUNACHAL PRADESH	27.264281	92.425854
West Khasi Hills	MEGHALAYA	25.518083	91.269445
West Nimar	MADHYA PRADESH	21.825248	75.61635
West Siang	ARUNACHAL PRADESH	28.168599	94.80047
West Tripura	TRIPURA	23.827795	91.274175
Wokha	NAGALAND	26.0917	94.258877
Yamunanagar	HARYANA	30.30369	77.307789
Yanam	PONDICHERRY	16.734771	82.213971
Yavatmal	MAHARASHTRA	20.3876	78.131472
Zunheboto	NAGALAND	26.009562	94.521241

sort them statewise and also tell me that is it complete or not
"""

# Load data into DataFrame
df = pd.read_csv(StringIO(data), sep='\t')

# Sort by State, then District
df_sorted = df.sort_values(['State', 'District'])

# Print the sorted DataFrame as tab-separated values
print(df_sorted.to_csv(sep='\t', index=False))