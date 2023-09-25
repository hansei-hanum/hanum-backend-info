# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nauth.proto\x12\x04\x61uth\"!\n\x10\x41uthorizeRequest\x12\r\n\x05token\x18\x01 \x01(\t\"B\n\x0f\x41uthorizeResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x13\n\x06userid\x18\x02 \x01(\x03H\x00\x88\x01\x01\x42\t\n\x07_userid\" \n\x0eGetUserRequest\x12\x0e\n\x06userid\x18\x01 \x01(\x03\"\x8d\x01\n\x0cVerification\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x12\n\ndepartment\x18\x02 \x01(\t\x12\r\n\x05grade\x18\x03 \x01(\x05\x12\x11\n\tclassroom\x18\x04 \x01(\x05\x12\x0e\n\x06number\x18\x05 \x01(\x05\x12\x13\n\x0bvalid_until\x18\x06 \x01(\t\x12\x14\n\x0cgraduated_at\x18\x07 \x01(\t\"\xaa\x01\n\x04User\x12\n\n\x02id\x18\x01 \x01(\x03\x12\r\n\x05phone\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07profile\x18\x05 \x01(\t\x12\x12\n\ncreated_at\x18\x06 \x01(\t\x12\x14\n\x0cis_suspended\x18\x07 \x01(\x08\x12-\n\x0cverification\x18\x08 \x01(\x0b\x32\x12.auth.VerificationH\x00\x88\x01\x01\x42\x0f\n\r_verification\"H\n\rGetUserResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x1d\n\x04user\x18\x02 \x01(\x0b\x32\n.auth.UserH\x00\x88\x01\x01\x42\x07\n\x05_user\"\x89\x01\n\x0fSendPushRequest\x12\x13\n\x06userid\x18\x01 \x01(\x03H\x00\x88\x01\x01\x12\x12\n\x05topic\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\r\n\x05title\x18\x03 \x01(\t\x12\x0c\n\x04\x62ody\x18\x04 \x01(\t\x12\r\n\x05image\x18\x05 \x01(\t\x12\x0c\n\x04link\x18\x06 \x01(\tB\t\n\x07_useridB\x08\n\x06_topic\"!\n\x0eSendPushResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\xbe\x01\n\x0b\x41uthService\x12<\n\tAuthorize\x12\x16.auth.AuthorizeRequest\x1a\x15.auth.AuthorizeResult\"\x00\x12\x36\n\x07GetUser\x12\x14.auth.GetUserRequest\x1a\x13.auth.GetUserResult\"\x00\x12\x39\n\x08SendPush\x12\x15.auth.SendPushRequest\x1a\x14.auth.SendPushResult\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'auth_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_AUTHORIZEREQUEST']._serialized_start=20
  _globals['_AUTHORIZEREQUEST']._serialized_end=53
  _globals['_AUTHORIZERESULT']._serialized_start=55
  _globals['_AUTHORIZERESULT']._serialized_end=121
  _globals['_GETUSERREQUEST']._serialized_start=123
  _globals['_GETUSERREQUEST']._serialized_end=155
  _globals['_VERIFICATION']._serialized_start=158
  _globals['_VERIFICATION']._serialized_end=299
  _globals['_USER']._serialized_start=302
  _globals['_USER']._serialized_end=472
  _globals['_GETUSERRESULT']._serialized_start=474
  _globals['_GETUSERRESULT']._serialized_end=546
  _globals['_SENDPUSHREQUEST']._serialized_start=549
  _globals['_SENDPUSHREQUEST']._serialized_end=686
  _globals['_SENDPUSHRESULT']._serialized_start=688
  _globals['_SENDPUSHRESULT']._serialized_end=721
  _globals['_AUTHSERVICE']._serialized_start=724
  _globals['_AUTHSERVICE']._serialized_end=914
# @@protoc_insertion_point(module_scope)
