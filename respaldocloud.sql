
use vendegram:
INSERT INTO `usuario` (`id`, `nombre`, `apellido`, `nombre_usuario`, `fecha_nacimiento`, `correo`, `telefono`, `clave_hash`, `salt`, `foto_perfil`, `administrador`, `suscripcion`, `fecha_registro`) VALUES
	(1, 'Oscar', 'Marino', 'oscarali', '1985-05-25', 'oscarali1985@gmail.com', '584126147743', 'pbkdf2:sha256:150000$MMzPQBBU$f30effe93ddc83b2d02eb46f37049d2a72125d6b135bb081166ff1128a7f5b7d', 'oFQ7bA==', 'Sinfoto', 1, NULL, '2020-10-06'),


INSERT INTO `tienda` (`id`, `nombre_tienda`, `correo_tienda`, `telefono_tienda`, `foto_tienda`, `facebook_tienda`, `instagram_tienda`, `twitter_tienda`, `zona_general`, `zona_uno`, `zona_dos`, `zona_tres`, `usuario_id`) VALUES
	(1, 'Support OAMD', 'oamd@gmail.com', '4241541455', NULL, 'oscarali', 'oscarali1985', NULL, 'DISTRITO_CAPITAL', 'Chacao', NULL, NULL, 1);
  (2, 'Vendegram', 'vendegram@gmail.com', '4241541455', NULL, '', '', NULL, 'DISTRITO_CAPITAL', 'Chacao', NULL, NULL, 2);
  
  INSERT INTO `tienda` (`id`, `nombre_tienda`, `correo_tienda`, `telefono_tienda`, `foto_tienda`, `facebook_tienda`, `instagram_tienda`, `twitter_tienda`, `zona_general`, `zona_uno`, `zona_dos`, `zona_tres`, `usuario_id`) VALUES
  (2, 'Vendegram', 'vendegram@gmail.com', '4241541455', NULL, '', '', NULL, 'DISTRITO_CAPITAL', 'Chacao', NULL, NULL, 2);