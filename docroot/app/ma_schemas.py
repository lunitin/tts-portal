from ma import ma
from .models import Vehicle, User, Coverage, Signal


class VehicleSchema(ma.SQLAlcehmyAutoSchema)
    class Meta:
        model = Vehicle
        load_instance = True
        include_fk = True


class UserSchema(ma.SQLAlcehmyAutoSchema)
    class Meta:
        model = User
        load_instance = True


class CoverageSchema(ma.SQLAlcehmyAutoSchema)
    class Meta:
        model = Coverage
        load_instance = True
        include_relationship = True
        
        
class SignalSchema(ma.SQLAlcehmyAutoSchema)
    class Meta:
        model = Signal
        load_instance = True
        include_fk = True
        include_relationship = True