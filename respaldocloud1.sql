-- --------------------------------------------------------
-- Host:                         bcslpycfmnhs9gp1fcfb-mysql.services.clever-cloud.com
-- Server version:               8.0.15-5 - Exherbo
-- Server OS:                    Linux
-- HeidiSQL Version:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for bcslpycfmnhs9gp1fcfb
CREATE DATABASE IF NOT EXISTS `bcslpycfmnhs9gp1fcfb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `bcslpycfmnhs9gp1fcfb`;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.alembic_version
CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.alembic_version: ~1 rows (approximately)
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` (`version_num`) VALUES
	('cbfadd2df132');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.producto
CREATE TABLE IF NOT EXISTS `producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `foto` varchar(200) NOT NULL,
  `descripcion` varchar(2000) NOT NULL,
  `precio` float NOT NULL,
  `cantidad` int(11) NOT NULL,
  `etiqueta_general` enum('PRODUCTOS','SERVICIOS') NOT NULL,
  `etiqueta_uno` enum('ALIMENTOS','BEBIDAS','CEREALES','DECORACIONES','DETERGENTES','ENLATADOS','JABONES','MANTENIMIENTOS','MAQUILLAJES','MEDICAMENTOS','PELUQUERIA','PELUQUERIA_VETERINARIA','PLOMERIA','REPARACIONES','ROPA','SALSAS') NOT NULL,
  `etiqueta_dos` enum('ALIMENTOS','BEBIDAS','CEREALES','DECORACIONES','DETERGENTES','ENLATADOS','JABONES','MANTENIMIENTOS','MAQUILLAJES','MEDICAMENTOS','PELUQUERIA','PELUQUERIA_VETERINARIA','PLOMERIA','REPARACIONES','ROPA','SALSAS') DEFAULT NULL,
  `etiqueta_tres` enum('ALIMENTOS','BEBIDAS','CEREALES','DECORACIONES','DETERGENTES','ENLATADOS','JABONES','MANTENIMIENTOS','MAQUILLAJES','MEDICAMENTOS','PELUQUERIA','PELUQUERIA_VETERINARIA','PLOMERIA','REPARACIONES','ROPA','SALSAS') DEFAULT NULL,
  `tienda_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `titulo` (`titulo`),
  KEY `tienda_id` (`tienda_id`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`tienda_id`) REFERENCES `tienda` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.producto: ~10 rows (approximately)
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` (`id`, `titulo`, `foto`, `descripcion`, `precio`, `cantidad`, `etiqueta_general`, `etiqueta_uno`, `etiqueta_dos`, `etiqueta_tres`, `tienda_id`) VALUES
	(1, 'Soporte Remoto PC', 'null', 'Se ofrece soporte remoto para revision de PC', 20, 10, 'SERVICIOS', 'REPARACIONES', NULL, NULL, 1),
	(2, 'Soporte Remoto PBX AVAYA', 'null', 'Tecnico en soluciones AVAYA', 40, 10, 'SERVICIOS', 'REPARACIONES', NULL, NULL, 1),
	(3, 'Soluciones en Hosting, dominios y Panel', 'null', 'Si quieres montar tu pagina y necesitas ayuda escribime y te cotizamos tu servicio', 40, 10, 'SERVICIOS', 'REPARACIONES', NULL, NULL, 1),
	(4, 'Venta de franelas Roxy y Quiksilver ', 'null', '', 12, 10, 'PRODUCTOS', 'ROPA', NULL, NULL, 1),
	(5, 'Harina pan por bulto', 'null', '', 12, 10, 'PRODUCTOS', 'ALIMENTOS', NULL, NULL, 1),
	(6, 'Ron El Toro', 'null', 'Venta de ron por unidad y cajas', 12, 10, 'PRODUCTOS', 'BEBIDAS', NULL, NULL, 1),
	(7, 'Harina PAN', 'null', 'Venta de Harina de maiz precocida Harina PAN solo por bulto', 12, 10, 'PRODUCTOS', 'ALIMENTOS', NULL, NULL, 1),
	(8, 'Zucaritas', 'null', 'Venta de Cereales Zucaritas', 12, 10, 'PRODUCTOS', 'ALIMENTOS', NULL, 'CEREALES', 1),
	(9, 'Te Gusta Nuestra Pagina', 'null', 'Somos el equipo que desarrollo este sistema todo desde cero, Si te gusta y deseas tener una pagina o un bot como el de nosotros escribenos', 0, 10, 'SERVICIOS', 'MANTENIMIENTOS', NULL, NULL, 5),
	(10, 'Desarrollo Full Stack', 'null', 'Si te gustaria colocar tu tienda en la web y adicionalmente tener un registro de tus clientes escribenos tu requerimiento y con gusto te mandamos un presupuesto', 0, 10, 'SERVICIOS', 'MANTENIMIENTOS', NULL, NULL, 5);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.producto_image
CREATE TABLE IF NOT EXISTS `producto_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(80) NOT NULL,
  `image_url` varchar(500) NOT NULL,
  `public_id` varchar(500) NOT NULL,
  `producto_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `image_url` (`image_url`),
  UNIQUE KEY `public_id` (`public_id`),
  UNIQUE KEY `unique_img_title_producto` (`title`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `producto_image_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.producto_image: ~0 rows (approximately)
/*!40000 ALTER TABLE `producto_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto_image` ENABLE KEYS */;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.suscripcion
CREATE TABLE IF NOT EXISTS `suscripcion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan` enum('BASICO') NOT NULL,
  `fecha_registro` date DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `suscripcion_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.suscripcion: ~0 rows (approximately)
/*!40000 ALTER TABLE `suscripcion` DISABLE KEYS */;
/*!40000 ALTER TABLE `suscripcion` ENABLE KEYS */;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.tienda
CREATE TABLE IF NOT EXISTS `tienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_tienda` varchar(40) NOT NULL,
  `correo_tienda` varchar(30) NOT NULL,
  `telefono_tienda` varchar(30) DEFAULT NULL,
  `foto_tienda` varchar(200) DEFAULT NULL,
  `facebook_tienda` varchar(30) DEFAULT NULL,
  `instagram_tienda` varchar(30) DEFAULT NULL,
  `twitter_tienda` varchar(30) DEFAULT NULL,
  `zona_general` enum('DISTRITO_CAPITAL','MIRANDA') NOT NULL,
  `zona_uno` enum('ALTAGRACIA','ANTÍMANO','CANDELARIA','CARICUAO','CATEDRAL','CATIA','CAUCAGÜITA','CHACAO','COCHE','EL_CAFETAL','EL_JUNQUITO','EL_PARAÍSO','EL_RECREO','EL_VALLE','FILA_DE_MARICHES','LA_DOLORITA','LA_PASTORA','LA_VEGA','LAS_MINAS','LEONCIO_MARTÍNEZ','MACARAO','NUESTRA_SEÑORA_DEL_ROSARIO','PETARE','SAN_AGUSTÍN','SAN_BERNARDINO','SAN_JOSÉ','SAN_JUAN','SAN_PEDRO','SANTA_ROSALÍA','SANTA_ROSALÍA_DE_PALERMO','SANTA_TERESA','VEINTITRÉS_DE_ENERO') DEFAULT NULL,
  `zona_dos` enum('ALTAGRACIA','ANTÍMANO','CANDELARIA','CARICUAO','CATEDRAL','CATIA','CAUCAGÜITA','CHACAO','COCHE','EL_CAFETAL','EL_JUNQUITO','EL_PARAÍSO','EL_RECREO','EL_VALLE','FILA_DE_MARICHES','LA_DOLORITA','LA_PASTORA','LA_VEGA','LAS_MINAS','LEONCIO_MARTÍNEZ','MACARAO','NUESTRA_SEÑORA_DEL_ROSARIO','PETARE','SAN_AGUSTÍN','SAN_BERNARDINO','SAN_JOSÉ','SAN_JUAN','SAN_PEDRO','SANTA_ROSALÍA','SANTA_ROSALÍA_DE_PALERMO','SANTA_TERESA','VEINTITRÉS_DE_ENERO') DEFAULT NULL,
  `zona_tres` enum('ALTAGRACIA','ANTÍMANO','CANDELARIA','CARICUAO','CATEDRAL','CATIA','CAUCAGÜITA','CHACAO','COCHE','EL_CAFETAL','EL_JUNQUITO','EL_PARAÍSO','EL_RECREO','EL_VALLE','FILA_DE_MARICHES','LA_DOLORITA','LA_PASTORA','LA_VEGA','LAS_MINAS','LEONCIO_MARTÍNEZ','MACARAO','NUESTRA_SEÑORA_DEL_ROSARIO','PETARE','SAN_AGUSTÍN','SAN_BERNARDINO','SAN_JOSÉ','SAN_JUAN','SAN_PEDRO','SANTA_ROSALÍA','SANTA_ROSALÍA_DE_PALERMO','SANTA_TERESA','VEINTITRÉS_DE_ENERO') DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo_tienda` (`correo_tienda`),
  UNIQUE KEY `nombre_tienda` (`nombre_tienda`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `tienda_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.tienda: ~2 rows (approximately)
/*!40000 ALTER TABLE `tienda` DISABLE KEYS */;
INSERT INTO `tienda` (`id`, `nombre_tienda`, `correo_tienda`, `telefono_tienda`, `foto_tienda`, `facebook_tienda`, `instagram_tienda`, `twitter_tienda`, `zona_general`, `zona_uno`, `zona_dos`, `zona_tres`, `usuario_id`) VALUES
	(1, 'Support OAMD', 'oamd@gmail.com', '4241541455', NULL, 'oscarali', 'oscarali1985', NULL, 'MIRANDA', 'CHACAO', NULL, NULL, 1),
	(2, 'Vendegram', 'vendegram@gmail.com', '4241541455', NULL, '', '', NULL, 'MIRANDA', 'CHACAO', NULL, NULL, 2);
/*!40000 ALTER TABLE `tienda` ENABLE KEYS */;

-- Dumping structure for table bcslpycfmnhs9gp1fcfb.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `nombre_usuario` varchar(20) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `correo` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `clave_hash` varchar(250) NOT NULL,
  `salt` varchar(16) NOT NULL,
  `foto_perfil` varchar(50) DEFAULT NULL,
  `administrador` tinyint(1) NOT NULL,
  `suscripcion` int(11) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- Dumping data for table bcslpycfmnhs9gp1fcfb.usuario: ~10 rows (approximately)
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` (`id`, `nombre`, `apellido`, `nombre_usuario`, `fecha_nacimiento`, `correo`, `telefono`, `clave_hash`, `salt`, `foto_perfil`, `administrador`, `suscripcion`, `fecha_registro`) VALUES
	(1, 'Oscar', 'Marino', 'oscarali', '1985-05-25', 'oscarali1985@gmail.com', '584126147743', 'pbkdf2:sha256:150000$dy8XtUSX$f20df039e6f789e9bcc0700c7d324dbfb6498ea77cd47aec2c296202004f0af4', 'K/8n8Q==', 'Sinfoto', 1, NULL, '2020-10-12'),
	(2, 'Vende', 'Gram', 'vendegram', '2020-10-01', 'vendegram@gmail.com', '584241541455', 'pbkdf2:sha256:150000$YO7alRFl$dcd4575cffc2e34620705397628e88829a87dab36237a299323dc7c53e0292bc', 'R4N//A==', 'Sinfoto', 1, NULL, '2020-10-13');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

