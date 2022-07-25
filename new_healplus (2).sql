-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 10, 2022 at 08:46 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `new_healplus`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_login`
--

CREATE TABLE `admin_login` (
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin_login`
--

INSERT INTO `admin_login` (`email`, `password`, `role`) VALUES
('tripathysonu59@gmail.com', 'sonu143', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `ap_doctor`
--

CREATE TABLE `ap_doctor` (
  `date` date NOT NULL,
  `doctor_name` text NOT NULL,
  `doctor_department` varchar(100) NOT NULL,
  `patient_name` text NOT NULL,
  `patient_age` int(11) NOT NULL,
  `patient_bloodgroup` varchar(2) NOT NULL,
  `patient_gender` text NOT NULL,
  `patient_mobile` varchar(11) NOT NULL,
  `patient_email` varchar(500) NOT NULL,
  `patient_address` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ap_doctor`
--

INSERT INTO `ap_doctor` (`date`, `doctor_name`, `doctor_department`, `patient_name`, `patient_age`, `patient_bloodgroup`, `patient_gender`, `patient_mobile`, `patient_email`, `patient_address`) VALUES
('2022-05-06', 'ASHISH TRIPATHY', 'Medicine', 'Sonu Sharma', 24, 'B+', 'Male', '09556406021', 'ashishtripathy58@gmail.com', 'KAUPARA'),
('2022-05-06', 'Dinesh Mishra', 'Medicine', 'Ashish Tripathy', 24, 'B+', 'Male', '09556406021', 'ashishtripathy58@gmail.com', 'KAUPARA'),
('2022-05-09', 'ASHISH TRIPATHY', 'Medicine', 'Sangeeta Dikshit', 24, 'B+', 'Female', '6370600381', 'sangeetadikshit58@gmail.com', 'Aul');

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `shift` varchar(10) NOT NULL,
  `intime` time(6) NOT NULL,
  `late` varchar(10) NOT NULL,
  `outtime` time(6) NOT NULL,
  `earlyleaving` time(6) NOT NULL,
  `overtime` varchar(100) NOT NULL,
  `totaltime` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`id`, `name`, `date`, `shift`, `intime`, `late`, `outtime`, `earlyleaving`, `overtime`, `totaltime`) VALUES
(3, 'ASHISH TRIPATHY', '2022-05-09', '3pm-11pm', '15:48:41.000000', '48min', '00:00:00.000000', '00:00:00.000000', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `billing`
--

CREATE TABLE `billing` (
  `id` int(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `mobile` varchar(13) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `p_name` varchar(100) NOT NULL,
  `p_id` varchar(100) NOT NULL,
  `quantity` int(100) NOT NULL,
  `price_unit` varchar(100) NOT NULL,
  `with_gst` varchar(100) NOT NULL,
  `total_price` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `billing`
--

INSERT INTO `billing` (`id`, `name`, `mobile`, `email`, `address`, `date`, `p_name`, `p_id`, `quantity`, `price_unit`, `with_gst`, `total_price`) VALUES
(14, 'ASHISH TRIPATHY', '9556406021', 'ashishtripathy58@gmail.com', 'KAUPARA', '2022-04-20', 'Biscuit', '15546', 10, '25', '4.5', '254.5'),
(15, 'ASHISH TRIPATHY', '09556406021', 'ashishtripathy58@gmail.com', 'KAUPARA', '2022-05-06', 'Biscuit', '15546', 10, '99', '17.82', '1007.82');

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `email` varchar(200) NOT NULL,
  `specialization` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `age` int(10) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `bloodgroup` varchar(5) NOT NULL,
  `address` varchar(500) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`id`, `d_id`, `name`, `phone`, `email`, `specialization`, `department`, `age`, `gender`, `bloodgroup`, `address`, `status`) VALUES
(8, 123, 'Dr. Chiku', '6370375724', 'manoranjanmuduli101@gmail.com', 'Opd Doctors', 'Eye Opd', 24, 'Male', 'A+', 'Narasinghpur, Cuttack', 'Available');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `e_id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `gender` text NOT NULL,
  `phone` varchar(11) NOT NULL,
  `dob` varchar(10) NOT NULL,
  `bloodgroup` varchar(3) NOT NULL,
  `age` int(11) NOT NULL,
  `designation` text NOT NULL,
  `department` varchar(100) NOT NULL,
  `photo` varchar(1000) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `e_id`, `name`, `email`, `address`, `gender`, `phone`, `dob`, `bloodgroup`, `age`, `designation`, `department`, `photo`, `status`) VALUES
(24, 9556, 'ASHISH TRIPATHY', 'ashishtripathy58@gmail.com', 'KAUPARA', 'Male', '9556406021', '18-03-1998', 'B+', 24, 'Super Specialist', 'Medicine', 'WhatsApp_Image_2021-03-29_at_2.33.55_PM.jpeg', 'Available'),
(27, 8889, 'Manoranjan Muduli', 'manoranjanmuduli101@gmail.com', 'Cuttack', 'Male', '6370375724', '17-05-1998', 'B+', 24, 'Doctor', 'Urology', 'WhatsApp_Image_2022-05-04_at_2.08.49_PM.jpeg', 'Available'),
(28, 7978, 'Dinesh Mishra', 'dinkumar146@gmail.com', 'Mayurbhanj', 'Male', '7978226068', '04/08/1998', 'A-', 24, 'Specialist', 'Medicine', 'WhatsApp_Image_2022-05-04_at_2.10.47_PM_1.jpeg', 'Available'),
(29, 8585, 'Jyoti Ranjan Das', 'jrd@gmail.com', 'Bbsr', 'Male', '7008945177', '18-03-1998', 'B+', 24, 'Doctor', 'Eye Opd', 'WhatsApp_Image_2022-05-04_at_2.10.47_PM.jpeg', 'Available'),
(30, 2005, 'Rohan Padhan', 'rohanpadhan240@gmail.com', 'Bargarh,Odisha', 'Male', '9337926798', '17/04/1999', 'O+', 23, 'Surgeon', 'Eye Opd', 'WhatsApp_Image_2022-05-04_at_2.10.47_PM_3.jpeg', 'Available'),
(31, 9348, 'Mir Meherban Ali', 'alkida@gmail.com', 'Salipur,Cuttack', 'Male', '9348748009', '17-05-1998', 'a+', 24, 'Super Specialist', 'Neurology', 'WhatsApp_Image_2022-05-04_at_2.10.47_PM_2.jpeg', 'Available');

-- --------------------------------------------------------

--
-- Table structure for table `middle_ware`
--

CREATE TABLE `middle_ware` (
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `middle_ware`
--

INSERT INTO `middle_ware` (`email`, `password`, `role`) VALUES
('sangeetadikshit58@gmail.com', 'at143', 'others');

-- --------------------------------------------------------

--
-- Table structure for table `online_appointment`
--

CREATE TABLE `online_appointment` (
  `id` int(11) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `email` varchar(200) NOT NULL,
  `gender` varchar(100) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `name` varchar(200) NOT NULL,
  `address` varchar(5000) NOT NULL,
  `age` int(2) NOT NULL,
  `problem` varchar(10000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `online_appointment`
--

INSERT INTO `online_appointment` (`id`, `mobile`, `email`, `gender`, `date`, `name`, `address`, `age`, `problem`) VALUES
(50, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-16', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'jhvgcrdxbjvctxt'),
(51, '9090970157', 'sahooaditya370@gmail.com', 'Male', '2022-04-15', 'Aditya Sahoo', 'KAUPARA', 24, 'kbaygcya cvwysc'),
(61, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-17', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(62, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-18', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(63, '7978226068', 'dk@gmail.com', 'Male', '2022-04-18', 'DInesh Mishra', 'Gadho,Mayurbhanj', 24, 'problems'),
(64, '9556406022', 'tripathysonu59@gmail.com', 'Male', '2022-04-18', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(65, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-19', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(66, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-19', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(67, '7978226068', 'tripathysonu59@gmail.com', 'Female', '2022-04-19', 'DInesh Mishra', 'Gadho,Mayurbhanj', 24, 'problems'),
(88, '7978226068', 'dk@gmail.com', 'Male', '2022-04-20', 'DInesh Mishra', 'KAUPARA', 25, 'problems'),
(89, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-20', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(90, '9090970157', 'aditya@gmail.com', 'Male', '2022-04-20', 'Aditya Sahoo', 'Patia, Bhubaneswar', 24, 'jhvgcrdxbjvctxt'),
(91, '7978365066', 'sahooaditya370@gmail.com', 'Male', '2022-04-20', 'Divine Ai', 'Patia, Bhubaneswar', 24, 'problems in eyes'),
(92, '7978365066', 'sahooaditya370@gmail.com', 'Male', '2022-04-20', 'Divine Ai', 'Patia, Bhubaneswar', 24, 'problems in eyes'),
(93, '9087899787', 'alkida@gmail.com', 'Male', '2022-04-20', 'Ali ', 'Salipur', 24, 'problems'),
(94, '9087899787', 'alkida@gmail.com', 'Male', '2022-04-20', 'Ali ', 'Salipur', 24, 'problems'),
(95, '7878676745', 'dk@gmail.com', 'Male', '2022-04-20', 'Aditya Sahoo', 'ke', 55, 'problems'),
(96, '9090970157', 'ashishtripathy58@gmail.com', 'Male', '2022-04-20', 'bshbsh', 'KAUPARA', 55, 'bxhgsh'),
(97, '0955640602', 'ashishtripathy58@gmail.com', 'Male', '2022-04-22', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(98, '7978226068', 'dk@gmail.com', 'Male', '2022-04-21', 'DInesh Mishra', 'KAUPARA', 24, 'problems'),
(99, '7877812345', 'alkida@gmail.com', 'Male', '2022-04-22', 'Ali ', 'Salipur', 24, 'jhvgcrdxbjvctxt'),
(100, '7978258096', 'dk@gmail.com', 'Male', '2022-04-22', 'Manoranjan Muduli', 'KAUPARA', 55, 'hgydxrsxh hgctdtchgyxt'),
(101, '0955640602', 'tripathysonu59@gmail.com', 'Male', '2022-04-22', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(102, '9556406021', 'ashishtripathy58@gmail.com', '', '2022-04-21', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(103, '9556406021', 'ashishtripathy58@gmail.com', '', '2022-04-21', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(104, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-21', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(105, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-21', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'i have problems in my eyes'),
(106, '7978226068', 'ashishtripathy58@gmail.com', '', '2022-04-21', 'DInesh Mishra', 'Gadho,Mayurbhanj', 24, 'problems'),
(107, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-21', 'ASHISH TRIPATHY', 'KAUPARA', 55, ',mx'),
(108, '0955640602', 'alkida@gmail.com', 'Male', '2022-04-21', 'Ali ', 'KAUPARA', 24, 'problems'),
(109, '0955640602', 'alkida@gmail.com', 'Female', '2022-04-21', 'Ali ', 'KAUPARA', 24, 'problems'),
(110, '0955640602', 'alkida@gmail.com', 'Female', '2022-04-21', 'Ali ', 'KAUPARA', 55, 'problems'),
(111, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-04-27', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(112, '9556406021', 'tripathysonu59@gmail.com', 'Male', '2022-04-28', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(113, '9556406021', 'ashishtripathy58@gmail.com', 'Male', '2022-05-02', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(114, '0955640602', 'tripathysonu59@gmail.com', 'Male', '2022-05-02', 'ASHISH TRIPATHY', 'KAUPARA', 24, 'problems'),
(115, '7978226068', 'dk@gmail.com', 'Female', '2022-05-02', 'Ali ', 'Salipur,Cuttack', 55, 'jhvgcrdxbjvctxt'),
(116, '6370375724', 'manoranjanmuduli101@gmail.com', 'Male', '2022-05-10', 'Chiku', 'Narasinghpur, Cuttack', 24, 'Body Pain');

-- --------------------------------------------------------

--
-- Table structure for table `other_staff`
--

CREATE TABLE `other_staff` (
  `email` varchar(200) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `other_staff`
--

INSERT INTO `other_staff` (`email`, `password`, `role`) VALUES
('devilisback226@gmail.com', 'Ashish@143', 'others');

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `code` varchar(20) NOT NULL,
  `name` text NOT NULL,
  `file` varchar(100) NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `search_metadata` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`code`, `name`, `file`, `price`, `quantity`, `search_metadata`) VALUES
('12345', 'DICLOPHINAC', 'bitcoin.jpeg', 12, 18, 'For body pain.'),
('3DcAM01', 'Crocin 650', 'Crocin.png', 30, 30, 'fever headache bodypain backpain'),
('e2ed', 'Paracetamol Tablet', 'Paracetamol.jpg', 10, 30, 'Fever Headache Muscle Pain Menstrual Cramps Post Immunization Pyrexia Arthritis'),
('ffgsd', 'Honitus', 'Honitus.png', 80, 30, 'Cough'),
('jliy6', 'Strepsils', 'strepsils.jpg', 6, 30, 'mouth throat infections'),
('LPN45', 'Aspirin', 'aspirin.jpg', 3, 30, 'headaches period pains colds flu sprains strains arthritis'),
('nijd7an', 'Combiflam', 'Combiflam.jpg', 29, 30, 'Fever Pain Menstrual Cramps Osteoarthritis Rheumatoid Arthritis Gout'),
('USB02', 'Gelusil', 'Gelusil.png', 88, 30, ' heartburn acid indigestion upset stomach bloating gas'),
('vnc3fb', 'Wikoryl Tablet', 'Wikoryl.jpg', 36.55, 30, 'Cold Common cold Fever Nasal decongestant Itchy throat/skin Headache Allergy Chill Toothache Ear pain Joint pain Periods pain Flu Hypotensive conditions Eye mydriasis Intraocular tension Hay fever Watery eyes Anaphylactic shock Rhinitis Urticaria');

-- --------------------------------------------------------

--
-- Table structure for table `slider`
--

CREATE TABLE `slider` (
  `name` varchar(10) NOT NULL,
  `sl1` varchar(1000) NOT NULL,
  `sl2` varchar(1000) NOT NULL,
  `sl3` varchar(1000) NOT NULL,
  `sl4` varchar(1000) NOT NULL,
  `content_sl1` varchar(1000) NOT NULL,
  `content_sl2` varchar(1000) NOT NULL,
  `content_sl3` varchar(1000) NOT NULL,
  `content_sl4` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `slider`
--

INSERT INTO `slider` (`name`, `sl1`, `sl2`, `sl3`, `sl4`, `content_sl1`, `content_sl2`, `content_sl3`, `content_sl4`) VALUES
('slider', 'banner1.jpg', 'banner2.jpg', 'banner3.jpg', 'banner4.jpg', 'Hii this is ashish', 'Welcome To Health Care Group', 'Its my choice', 'And u r here');

-- --------------------------------------------------------

--
-- Table structure for table `slots`
--

CREATE TABLE `slots` (
  `total_slot` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `slots`
--

INSERT INTO `slots` (`total_slot`) VALUES
(150);

-- --------------------------------------------------------

--
-- Table structure for table `super_admin_login`
--

CREATE TABLE `super_admin_login` (
  `email` varchar(300) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `super_admin_login`
--

INSERT INTO `super_admin_login` (`email`, `password`, `role`) VALUES
('manoranjanmuduli45@gmail.com', 'Chiku@123', 'super_admin');

-- --------------------------------------------------------

--
-- Table structure for table `tele_appointment`
--

CREATE TABLE `tele_appointment` (
  `id` int(11) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `WP_mobile` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mode` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `age` int(2) NOT NULL,
  `problem` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tele_appointment`
--

INSERT INTO `tele_appointment` (`id`, `mobile`, `WP_mobile`, `email`, `mode`, `department`, `date`, `name`, `address`, `age`, `problem`) VALUES
(1, '0955640602', '7749067578', 'ashishtripathy58@gmail.com', 'By Video Call', 'Gastroentology', '2022-04-08', 'Rohan Padhan', 'KAUPARA', 24, 'Gas');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `age` int(2) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `reffered_by` varchar(100) NOT NULL,
  `testname` varchar(100) NOT NULL,
  `unit` varchar(100) NOT NULL,
  `normalrange` varchar(100) NOT NULL,
  `reg_no` varchar(10) NOT NULL,
  `recv_on` date NOT NULL,
  `repo_on` date NOT NULL,
  `result` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`id`, `name`, `age`, `gender`, `reffered_by`, `testname`, `unit`, `normalrange`, `reg_no`, `recv_on`, `repo_on`, `result`) VALUES
(5, 'Ashish Tripathy', 30, '', '', '', '', '', '', '0000-00-00', '0000-00-00', 'No Status'),
(7, 'Chiku', 25, '', '', '', '', '', '', '0000-00-00', '0000-00-00', 'Report Ready'),
(8, 'Kumar Gourav', 12, 'Male', 'kg', 'Malaria', '2', '2', '2', '2022-04-21', '2022-04-21', 's'),
(9, 'Kumar Gourav', 12, 'Can\'t Say', 'kg', 'Dengue', '2', '2', '2', '2022-04-21', '2022-04-21', 's'),
(10, 'Kumar Gourav', 12, 'Can\'t Say', 'kg', 'Diabetes', '2', '2', '8', '2022-04-21', '2022-04-21', 's'),
(11, 'Aditya mc', 2, 'Trans', '2', 'Covid', '2', '2', '5', '2022-04-21', '2022-04-21', '2'),
(12, 'ASHISH TRIPATHY', 24, 'Male', 'Dr Ashish', 'Covid', '100', '100-120', '1501294193', '2022-04-22', '2022-04-22', 'bad');

-- --------------------------------------------------------

--
-- Table structure for table `user_login`
--

CREATE TABLE `user_login` (
  `name` varchar(100) NOT NULL,
  `email` varchar(200) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `password` varchar(100) NOT NULL,
  `confirm_password` varchar(100) NOT NULL,
  `gender` varchar(15) NOT NULL,
  `state` varchar(20) NOT NULL,
  `address` varchar(500) NOT NULL,
  `file_name` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user_login`
--

INSERT INTO `user_login` (`name`, `email`, `mobile`, `password`, `confirm_password`, `gender`, `state`, `address`, `file_name`) VALUES
('ASHISH TRIPATHY', 'ashishtripathy58@gmail.com', '9556406021', 'Sonu@143', 'Sonu@143', 'Male', 'ODISHA', 'KAUPARA', 'WhatsApp_Image_2021-03-29_at_2.34.03_PM.jpeg'),
('Manoranjan Muduli', 'manoranjanmuduli101@gmail.com', '6370375724', 'Chiku@123', 'Chiku@123', '', '', '', '5.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `billing`
--
ALTER TABLE `billing`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `online_appointment`
--
ALTER TABLE `online_appointment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `tele_appointment`
--
ALTER TABLE `tele_appointment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `billing`
--
ALTER TABLE `billing`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `online_appointment`
--
ALTER TABLE `online_appointment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=117;

--
-- AUTO_INCREMENT for table `tele_appointment`
--
ALTER TABLE `tele_appointment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
