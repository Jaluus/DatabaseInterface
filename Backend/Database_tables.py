from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class scan(db.Model):
    __tablename__ = "scan"
    __table_args__ = {"mysql_engine": "InnoDB"}
    _id = db.Column("id", db.BigInteger, unique=True, primary_key=True)
    name = db.Column("name", db.String(255), default="None", nullable=False)
    user = db.Column("user", db.String(255), nullable=False)
    time = db.Column("time", db.BigInteger, nullable=False)
    exfoliated_material = db.Column(
        "exfoliated_material", db.String(255), default="None", nullable=False
    )

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict["_sa_instance_state"]
        return model_dict

    def __init__(self, name, user, time, exfoliated_material):
        self.name = name
        self.user = user
        self.time = time
        self.exfoliated_material = exfoliated_material


class chip(db.Model):
    __tablename__ = "chip"
    __table_args__ = {"mysql_engine": "InnoDB"}
    _id = db.Column("id", db.BigInteger, unique=True, primary_key=True)
    scan_id = db.Column(
        "scan_id", db.BigInteger, db.ForeignKey("scan.id"), nullable=False
    )
    chip_thickness = db.Column(
        "chip_thickness", db.String(255), default="90nm", nullable=False
    )

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict["_sa_instance_state"]
        return model_dict

    def __init__(self, scan_id, chip_thickness="90nm"):
        self.scan_id = scan_id
        self.chip_thickness = chip_thickness


class flake(db.Model):
    __tablename__ = "flake"
    __table_args__ = {"mysql_engine": "InnoDB"}
    _id = db.Column("id", db.BigInteger, unique=True, primary_key=True)
    chip_id = db.Column(
        "chip_id", db.BigInteger, db.ForeignKey("chip.id"), nullable=False
    )
    position_x = db.Column("position_x", db.Float, nullable=False)
    position_y = db.Column("position_y", db.Float, nullable=False)
    size = db.Column("size", db.Float, nullable=False)
    thickness = db.Column("thickness", db.String(255), nullable=False)
    entropy = db.Column("entropy", db.Float, nullable=False)

    aspect_ratio = db.Column("aspect_ratio", db.Float, nullable=False)
    width = db.Column("width", db.Float, nullable=False)
    height = db.Column("height", db.Float, nullable=False)
    proximity_stddev = db.Column("proximity_stddev", db.Float, nullable=False)
    mean_contrast_r = db.Column("mean_contrast_r", db.Float, nullable=False)
    mean_contrast_g = db.Column("mean_contrast_g", db.Float, nullable=False)
    mean_contrast_b = db.Column("mean_contrast_b", db.Float, nullable=False)

    path = db.Column("path", db.String(255), nullable=False)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict["_sa_instance_state"]
        return model_dict

    # this has to be easier
    def __init__(
        self,
        chip_id: int,
        position_x: float,
        position_y: float,
        size: float,
        thickness,
        entropy: float,
        path: str,
        aspect_ratio: float = -1,
        width: float = -1,
        height: float = -1,
        proximity_stddev: float = -1,
        mean_contrast_r: float = -1,
        mean_contrast_g: float = -1,
        mean_contrast_b: float = -1,
    ):
        self.chip_id = chip_id
        self.size = size
        self.thickness = thickness
        self.position_x = position_x
        self.position_y = position_y
        self.entropy = entropy
        self.aspect_ratio = aspect_ratio
        self.width = width
        self.height = height
        self.proximity_stddev = proximity_stddev
        self.mean_contrast_r = mean_contrast_r
        self.mean_contrast_g = mean_contrast_g
        self.mean_contrast_b = mean_contrast_b
        self.path = path


class image(db.Model):
    __tablename__ = "image"
    __table_args__ = {"mysql_engine": "InnoDB"}
    _id = db.Column("id", db.BigInteger, unique=True, primary_key=True)
    flake_id = db.Column(
        "flake_id", db.BigInteger, db.ForeignKey("flake.id"), nullable=False
    )
    path = db.Column("path", db.String(255), nullable=False)
    aperture = db.Column("aperture", db.Float, nullable=False)
    light_voltage = db.Column("light_voltage", db.Float, nullable=False)
    magnification = db.Column("magnification", db.Float, nullable=False)
    white_balance_r = db.Column("white_balance_r", db.Integer, nullable=False)
    white_balance_g = db.Column("white_balance_g", db.Integer, nullable=False)
    white_balance_b = db.Column("white_balance_b", db.Integer, nullable=False)
    gain = db.Column("gain", db.Float, nullable=False)
    gamma = db.Column("gamma", db.Integer, nullable=False)
    exposure_time = db.Column("exposure_time", db.Float, nullable=False)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict["_sa_instance_state"]
        return model_dict

    def __init__(
        self,
        flake_id,
        path,
        aperture,
        light,
        nosepiece,
        white_balance,
        gain,
        gamma,
        exposure,
        **kwargs,
    ):
        self.flake_id = flake_id
        self.path = path
        self.aperture = aperture
        self.light_voltage = light
        self.magnification = nosepiece
        self.white_balance_r = white_balance[0]
        self.white_balance_g = white_balance[1]
        self.white_balance_b = white_balance[2]
        self.gain = gain
        self.exposure_time = exposure
        self.gamma = gamma
