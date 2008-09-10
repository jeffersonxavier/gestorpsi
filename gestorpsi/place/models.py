# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from gestorpsi.address.models import Address
from gestorpsi.phone.models import Phone
from django.contrib.contenttypes import generic
from gestorpsi.organization.models import Organization
from gestorpsi.util.uuid_field import UuidField

class PlaceType( models.Model ):
    """
    This class represents place types.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    description= models.CharField( max_length= 80 )
    
    def __unicode__(self):
        """
        Returns a representation of this place type as an unicode C{string}.
        """
        return "%s" % self.description

class Place( models.Model ):
    """
    This class represents a place.
    @author: Vinicius H. S. Durelli
    @version: 1.0
    """
    id = UuidField(primary_key=True)
    label= models.CharField( max_length= 80 )
    visible= models.BooleanField(blank=True)
    address= generic.GenericRelation( Address )
    phones= generic.GenericRelation( Phone )
    place_type= models.ForeignKey( PlaceType )
    organization = models.ForeignKey(Organization, null= True, blank= True)

    def __unicode__(self):
       """
       Returns a representation of this place as an unicode C{string}.
       """
       return "%s" % self.label
   
    def get_first_phone(self):
       if ( len( self.phones.all() ) != 0 ):
         return self.phones.all()[0]
       else:
         return ''
    
    class Meta:
        ordering = ['label']
        

class RoomType( models.Model ):
   """
   This class contains information on room types, thus instances of this class can be used to
   handle information related to room types.
   @author: Vinicius H. S. Durelli
   @version: 1.0
   """
   description= models.CharField( max_length= 45, unique= True )
   
   """
   Returns a representation of this room type as an unicode C{string}.
   """
   def __unicode__(self):
      return "%s" % self.description


class Room( models.Model ):
   """
   This class represents a room, it also holds information on the furniture that belongs to
   the underlying room and its dimension.
   @author: Vinicius H. S. Durelli
   @version: 1.0
   """
   id = UuidField(primary_key=True)
   description= models.CharField( max_length= 80, blank=True )
   dimension= models.IntegerField(null=True, blank=True)
   place= models.ForeignKey( Place )
   room_type= models.ForeignKey( RoomType, related_name= 'room_type' )
   furniture= models.TextField()
   class Meta:
       ordering = ['description']
   """
   Returns a representation of this room as an unicode C{string}.
   """
   def __unicode__(self):
      return "%s" % self.description
  
   def __cmp__(self, other):
      if (self.description == other.description ) and \
         (self.dimension == other.dimension ) and \
         (self.room_type.id == other.room_type.id ) and \
         (self.furniture == other.furniture ):
         return 0
      else:
         return 1

class RoomForm(ModelForm):
   class Meta:
      model= Room

class PlaceForm(ModelForm):
   class Meta:
       model= Place