/**
 * Decodes a JWT.
 * @description If the JWT can be decoded or is already decoded, the decoded JWT is returned, else null.
 */
export const decodeJwt = jwt => {
  if (typeof jwt === 'string') {
    return jwt ? JSON.parse(Buffer.from(jwt.split('.')[1], 'base64')) : null;
  }
  if (typeof jwt === 'object') {
    return jwt;
  }
  return null;
};

export const willJwtExpire = (jwt, secondsWithin = 0) => {
  const { exp = 0 } = decodeJwt(jwt);
  const expiresInMilliseconds = exp * 1000;
  const millisecondsWithin = secondsWithin * 1000;

  return expiresInMilliseconds - millisecondsWithin < Date.now();
};
